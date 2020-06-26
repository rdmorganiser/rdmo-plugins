import json
import mimetypes

from rdmo.domain.models import Attribute
from rdmo.projects.imports import Import
from rdmo.projects.models import Project, Value
from rdmo.questions.models import Catalog


class MaDMPImport(Import):

    def check(self):
        if mimetypes.guess_type('application/json'):
            try:
                with open(self.file_name) as f:
                    data = json.loads(f.read())
                    self.dmp = data.get('dmp')
            except json.decoder.JSONDecodeError:
                return False

            if self.dmp:
                return True

    def process(self):
        project = Project()

        project.title = self.dmp.get('title')
        project.description = self.dmp.get('description')
        project.created = self.dmp.get('created', '')
        project.catalog = Catalog.objects.first()

        values = []

        for set_index, dmp_dataset in enumerate(self.dmp['dataset']):
            if dmp_dataset.get('title'):
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/id'),
                    set_index=set_index,
                    text=dmp_dataset.get('title')
                ))

            if dmp_dataset.get('description'):
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/description'),
                    set_index=set_index,
                    text=dmp_dataset.get('description')
                ))

            for collection_index, text in enumerate(dmp_dataset.get('data_quality_assurance', [])):
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/quality_assurance'),
                    set_index=set_index,
                    collection_index=collection_index,
                    text=text
                ))

            dmp_dataset_id = dmp_dataset.get('dataset_id')
            if dmp_dataset_id:
                if dmp_dataset_id.get('identifier'):
                    values.append(Value(
                        attribute=self.get_attribute(path='project/dataset/identifier'),
                        set_index=set_index,
                        text=dmp_dataset_id.get('identifier')
                    ))
                if dmp_dataset_id.get('type'):
                    values.append(Value(
                        attribute=self.get_attribute(path='project/dataset/identifier_type'),
                        set_index=set_index,
                        text=dmp_dataset_id.get('type')
                    ))

        for set_index, dmp_project in enumerate(self.dmp.get('project', [])):
            pass

        # snapshots, tasks, and views are not part of madmp
        snapshots = []
        tasks = []
        views = []

        return project, values, snapshots, tasks, views

    def get_attribute(self, path):
        try:
            return Attribute.objects.get(path=path)
        except Attribute.DoesNotExist:
            return None
