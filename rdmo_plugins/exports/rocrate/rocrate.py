import json
from pathlib import Path
import tempfile

import toml
from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from rdmo.projects.exports import Export
from rdmo.services.providers import OauthProviderMixin

from rocrate.rocrate import ROCrate
from rocrate.model.person import Person


class ROCrateExport(OauthProviderMixin, Export):
    class Form(forms.Form):
        dataset = forms.CharField(label=_("Select dataset of your project"))

        def __init__(self, *args, **kwargs):
            dataset_choices = kwargs.pop("dataset_choices")
            super().__init__(*args, **kwargs)

            self.fields["dataset"].widget = forms.CheckboxSelectMultiple(
                choices=dataset_choices, attrs={"checked": "checked"}
            )

        def clean_dataset(self):
            data = self.data.getlist("dataset")
            data = list(map(int, data))
            return data

    def load_config(self, file_name):
        toml_file = Path(__file__).parent / file_name
        try:
            toml_dict = toml.loads(toml_file.read_bytes().decode())
            return toml_dict
        except FileNotFoundError as exc:
            raise exc from exc
        except Exception as exc:
            # TODO add toml.TOMLDecodeError later
            raise ValueError(
                "\nThe {} file is not a valid TOML file.\n\t{}".format(toml_file, exc)
            ) from exc

    def render(self):
        datasets = self.get_set("project/dataset/id")
        dataset_choices = [(dataset.set_index, dataset.value) for dataset in datasets]

        self.store_in_session(self.request, "dataset_choices", dataset_choices)

        form = self.Form(dataset_choices=dataset_choices)

        return render(
            self.request, "plugins/exports_rocrate.html", {"form": form}, status=200
        )

    def submit(self):
        dataset_choices = self.get_from_session(self.request, "dataset_choices")
        form = self.Form(self.request.POST, dataset_choices=dataset_choices)

        if "cancel" in self.request.POST:
            return redirect("project", self.project.id)

        if form.is_valid():
            config = self.load_config("default.toml")
            dataset_selection = form.cleaned_data["dataset"]
            temp_folder = self.get_rocrate(config, dataset_selection)

            file_contents = json.loads(
                Path(temp_folder / "ro-crate-metadata.json").read_text()
            )
            response = HttpResponse(
                json.dumps(file_contents, indent=2),
                content_type="application/json",
            )
            response["Content-Disposition"] = 'filename="%s.json"' % self.project.title
            return response
        else:
            return render(
                self.request, "plugins/exports_rocrate.html", {"form": form}, status=200
            )

    def get_rocrate(self, config, dataset_selection):
        crate = ROCrate()
        crate.name = self.project.title

        project_config = config.pop("project")
        project_config_text = self.get_text_values_from_project(project_config)
        for key, value in project_config_text.items():
            setattr(crate, key, value)

        datasets = {}
        persons = {}
        dataset_config = config.pop("dataset")
        dataset_person_config = config.pop("dataset_person")
        for set_index in dataset_selection:
            # get_rocrate_object_from_rdmo_project_dataset_id
            dataset = self.get_text_values_by_dataset(dataset_config, set_index)
            datasets[set_index] = dataset
            person = self.get_text_values_by_dataset(dataset_person_config, set_index)
            persons[set_index] = person

        rocrate_person_ids_by_dataset = {}
        for key, value in persons.items():
            ro_person = Person(crate, properties=value)
            if ro_person not in rocrate_person_ids_by_dataset.values():
                crate.add(ro_person)
                rocrate_person_ids_by_dataset[key] = {"@id": ro_person.id}

        temp_folder = Path(tempfile.gettempdir()) / "rocrate"
        temp_folder.mkdir(parents=True, exist_ok=True)
        for key, value in datasets.items():
            file_name = value.pop("file_name")

            value["author"] = rocrate_person_ids_by_dataset[key]
            folder_path = temp_folder / file_name
            crate.add_dataset(folder_path, properties=value)

        crate.write(temp_folder)
        crate.write_zip(temp_folder.with_suffix(".zip"))
        return temp_folder


    def get_text_from_item_list(self, values, set_index) -> str:
        for item in values:
            text = self.get_text(item, set_index=set_index)
            if text:
                return text


    def get_text_values_by_dataset(self, dataset_config, set_index) -> dict:
        result = {}
        dataset_config.update(
            {
                key: [value]
                for key, value in dataset_config.items()
                if isinstance(value, str)
            }
        )
        for key, value in dataset_config.items():
            text = self.get_text_from_item_list(value, set_index)
            if text is None:
                text = f"{key} #{str(set_index + 1)}"
            result[key] = text
        return result


    def get_text_values_from_project(self, project_config) -> dict:
        return {
            key: ", ".join(self.get_list(value))
            for key, value in project_config.items()
        }
