import json
from pathlib import Path
import tempfile

import toml
from django import forms
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from rdmo.projects.exports import Export

from rocrate.rocrate import ROCrate
from rocrate.model.person import Person

# Settings
try:
    WEB_PREVIEW = settings.ROCRATE_EXPORT_WEB_PREVIEW
except AttributeError:
    WEB_PREVIEW = False

CONFIG_FILE = "rdmo-rocrate.toml"


def load_config(file_name):
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


class ROCrateExport(Export):
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

    def render(self):
        datasets = self.get_set("project/dataset/id")
        dataset_choices = [(dataset.set_index, dataset.value) for dataset in datasets]

        self.request.session[f"{self.class_name}.dataset_choices"] = dataset_choices

        form = self.Form(dataset_choices=dataset_choices)
        if not dataset_choices:
            response = self.get_rocrate_response()
            return response

        return render(
            self.request,
            "plugins/exports_rocrate.html",
            {"form": form, "project_id": self.project.pk},
            status=200,
        )

    def submit(self):
        dataset_choices = self.request.session[f"{self.class_name}.dataset_choices"]

        form = self.Form(self.request.POST, dataset_choices=dataset_choices)

        if "cancel" in self.request.POST:
            return redirect("project", self.project.id)

        if form.is_valid():
            dataset_selection = form.cleaned_data.get("dataset", [])
            response = self.get_rocrate_response(dataset_selection)
            return response

        return render(
            self.request, "plugins/exports_rocrate.html", {"form": form}, status=200
        )

    def get_rocrate_response(self, dataset_selection=None) -> FileResponse:
        config = load_config(CONFIG_FILE)
        crate = self.create_rocrate(config, dataset_selection)

        if WEB_PREVIEW:
            temp_folder = Path(tempfile.gettempdir()) / "rocrate"
            crate.write(temp_folder)
            file_contents = json.loads(
                Path(temp_folder / "ro-crate-metadata.json").read_text()
            )
            response = FileResponse(
                json.dumps(file_contents, indent=2),
                content_type="application/json",
                as_attachment=False,
            )
            return response

        # zip export
        ZIP_FILE_NAME = slugify(self.project.title) + "_rocrate.zip"
        crate.write_zip(ZIP_FILE_NAME)
        response = FileResponse(
            open(ZIP_FILE_NAME, "rb"),
            as_attachment=True,
            content_type="application/zip",
        )
        return response

    def create_rocrate(self, config, dataset_selection=None):
        crate = ROCrate()
        crate.name = self.project.title

        project_config_text = self.get_text_values_from_project(config.pop("project"))
        for key, value in project_config_text.items():
            setattr(crate, key, value)

        datasets = self.collect_crate_data_for_selection(
            config.pop("dataset"), dataset_selection
        )
        persons = self.collect_crate_data_for_selection(
            config.pop("dataset_person"), dataset_selection
        )

        rocrate_person_ids_by_dataset = {}
        for key, value in persons.items():
            ro_person = Person(crate, properties=value)
            if ro_person not in rocrate_person_ids_by_dataset.values():
                crate.add(ro_person)
                rocrate_person_ids_by_dataset[key] = {"@id": ro_person.id}

        for key, value in datasets.items():
            file_name = value.pop("file_name")
            value["author"] = rocrate_person_ids_by_dataset[key]
            crate.add_dataset(dest_path=file_name, properties=value)

        return crate

    def collect_crate_data_for_selection(self, config, dataset_selection):
        data = {}
        if dataset_selection is None:
            return data
        for set_index in dataset_selection:
            dataset = self.get_text_values_by_dataset(config, set_index)
            data[set_index] = dataset
        return data

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
