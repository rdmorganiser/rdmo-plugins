import json
import tempfile
from collections import defaultdict
from os import makedirs
from os.path import isfile
from os.path import join as pj
from os.path import realpath

import toml
from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from rdmo.core.utils import import_class
from rdmo.projects.exports import Export
from rdmo.services.providers import OauthProviderMixin
from rocrate.rocrate import ROCrate


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

    def load_mapping(self, file_name):
        scriptname = realpath(__file__)
        scriptdir = "/".join(scriptname.split("/")[:-1])
        file_name_full = pj(scriptdir, file_name)
        if isfile(file_name_full) is False:
            print("toml file does not exist: " + file_name_full)
        else:
            with open(file_name_full) as filedata:
                try:
                    data = filedata.read()
                    d = toml.loads(data)
                    return d
                except Exception as e:
                    print("toml decode error: " + str(file_name_full))
                    raise (e)
        return None

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
            mapping = self.load_mapping("default.toml")
            temp_folder = self.get_rocrate(mapping, form.cleaned_data["dataset"])
            with open(pj(temp_folder, "ro-crate-metadata.json")) as json_file:
                file_contents = json.loads(json_file.read())
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

    def get_rocrate(self, mapping, dataset_selection):
        crate = ROCrate()
        crate.name = self.project.title
        # crate.description = self.project.description
        temp_folder = pj(tempfile.gettempdir(), "rocrate")
        self.iterate_root(
            temp_folder, crate, mapping, dataset_selection=dataset_selection
        )

        crate.write(temp_folder)
        crate.write_zip(temp_folder + ".zip")
        return temp_folder

    def iterate_root(self, crate_folder, crate, tree, dataset_selection=[]):
        datasets = {}
        persons = {}
        for key, value in tree.items():
            if isinstance(value, str):
                setattr(crate, key, ", ".join(self.get_list(value)))
            elif isinstance(value, list):
                for val in value:
                    db_val = self.get_list(val)
                    if db_val:
                        setattr(crate, key, ", ".join(db_val))
                        break
            elif isinstance(value, dict):
                if "dataset" in key:
                    for rdmo_dataset in self.get_set("project/dataset/id"):
                        set_index = rdmo_dataset.set_index
                        if set_index in dataset_selection:
                            node_properties = self.iterate_node(
                                crate, value, set_index=set_index
                            )

                            if "file_name" in node_properties:
                                file_name = node_properties.pop("file_name")
                                folder_path = pj(crate_folder, file_name)
                                makedirs(folder_path, exist_ok=True)

                            datasets[set_index] = getattr(crate, key)(
                                folder_path, properties=node_properties
                            )

                elif "person" in key:
                    for rdmo_persons in self.get_set("project/dataset/creator/name"):
                        set_index = rdmo_persons.set_index
                        if set_index in dataset_selection:
                            node_properties = self.iterate_node(
                                crate, value, set_index=set_index
                            )

                            found = False
                            for pers in persons.values():
                                try:
                                    node_properties["name"]
                                    pers.properties()["name"]
                                except:
                                    pass
                                else:
                                    if (
                                        node_properties["name"]
                                        == pers.properties()["name"]
                                    ):
                                        found = True
                                        persons[set_index] = pers
                                        break
                            if found is False:
                                persons[set_index] = crate.add(
                                    import_class(key)(crate, properties=node_properties)
                                )
                else:
                    self.iterate_node(crate_folder, crate, value, key)
            else:
                raise ValueError("Expected string or list as value for ro crate config")

        for set_index, dataset in datasets.items():
            if set_index in persons:
                dataset["author"] = persons[set_index]

    def iterate_node(self, crate, tree, set_index=None):
        node_properties = {}
        for key, value in tree.items():
            if isinstance(value, str):
                node_properties[key] = ", ".join(
                    self.get_list(value, set_index=set_index)
                )
            elif isinstance(value, list):
                for val in value:
                    db_val = self.get_list(val, set_index=set_index)
                    if db_val:
                        node_properties[key] = ", ".join(db_val)
                        break
            elif isinstance(value, dict):
                self.iterate_node(crate, value, key, set_index=set_index)
            else:
                raise ValueError("Expected string or list as value for ro crate config")
        return node_properties

    def get_datasets(self):
        datasets = []
        for rdmo_dataset in self.get_set("project/dataset/id"):
            set_index = rdmo_dataset.set_index
            dataset = defaultdict(list)

            dataset["file_name"] = "{}".format(
                self.get_text("project/dataset/identifier", set_index=set_index)
                or self.get_text("project/dataset/id", set_index=set_index)
                or str(set_index + 1)
            )

            dataset["title"] = (
                self.get_text("project/dataset/title", set_index=set_index)
                or self.get_text("project/dataset/id", set_index=set_index)
                or "Dataset #{}".format(set_index + 1)
            )

            description = self.get_text(
                "project/dataset/description", set_index=set_index
            )
            if description:
                dataset["description"] = description

            datasets.append(dataset)

        return datasets

    def get_name(self, attribute, set_prefix="", set_index=0):
        name_text = self.get_text(
            attribute + "/name", set_prefix=set_prefix, set_index=set_index
        )
        if name_text:
            name = {
                "name": name_text,
                "nameType": self.get_option(
                    self.name_type_options,
                    attribute + "/name_type",
                    set_prefix=set_prefix,
                    set_index=set_index,
                    default="Personal",
                ),
            }

            # contributor_name
            contributor_type = self.get_option(
                self.contributor_type_options,
                attribute + "/contributor_type",
                set_prefix=set_prefix,
                set_index=set_index,
                default="Other",
            )
            if contributor_type:
                name["contributorType"] = contributor_type

            # given_name
            given_name = self.get_text(
                attribute + "/given_name", set_prefix=set_prefix, set_index=set_index
            )
            if given_name:
                name["givenName"] = given_name

            # family_name
            family_name = self.get_text(
                attribute + "/family_name", set_prefix=set_prefix, set_index=set_index
            )
            if family_name:
                name["familyName"] = family_name

            # identifier
            identifier = self.get_text(
                attribute + "/name_identifier",
                set_prefix=set_prefix,
                set_index=set_index,
            )
            if identifier:
                name["nameIdentifier"] = identifier
                name["nameIdentifierScheme"] = self.get_option(
                    self.name_identifier_scheme_options,
                    attribute + "/name_identifier_scheme",
                    set_prefix=set_prefix,
                    set_index=set_index,
                    default="ORCID",
                )

            # affiliations
            affiliations = self.get_list(
                attribute + "/affiliation", set_prefix=set_prefix, set_index=set_index
            )
            if affiliations:
                name["affiliations"] = []
                for affiliation in affiliations:
                    name["affiliations"].append({"affiliation": affiliation})

            return name
        else:
            return None
