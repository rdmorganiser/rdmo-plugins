import json
import mimetypes

from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.projects.imports import Import
from rdmo.projects.models import Project, Value
from rdmo.questions.models import Catalog


class MaDMPImport(Import):

    yes_no = {
        'yes': '1',
        'no': '0'
    }

    language_options = {
        # 'eng': '',
        # 'deu': ''
    }

    def check(self):
        if mimetypes.guess_type('application/json'):
            try:
                with open(self.file_name) as f:
                    data = json.loads(f.read())
                    self.dmp = data.get('dmp')
                    print(self.dmp)
            except json.decoder.JSONDecodeError:
                return False

            if self.dmp:
                return True

    def process(self):
        project = Project()

        project.title = self.dmp.get('title')
        project.description = self.dmp.get('description', '')
        project.created = self.dmp.get('created', '')
        project.catalog = Catalog.objects.first()

        values = []

        dmp_contact = self.dmp.get('contact')
        if dmp_contact:
            if dmp_contact.get('name'):
                attribute = self.get_attribute(path='project/dmp/contact/name')
                values.append(Value(
                    attribute=attribute,
                    text=dmp_contact.get('name')
                ))
            if dmp_contact.get('mbox'):
                attribute = self.get_attribute(path='project/dmp/contact/mbox')
                values.append(Value(
                    attribute=attribute,
                    text=dmp_contact.get('mbox')
                ))
            dmp_contact_id = dmp_contact.get('contact_id')
            if dmp_contact_id.get('identifier'):
                attribute = self.get_attribute(path='project/dmp/contact/identifier')
                values.append(Value(
                    attribute=attribute,
                    text=dmp_contact.get('identifier')
                ))
            if dmp_contact_id.get('type'):
                attribute = self.get_attribute(path='project/dmp/contact/identifier_type')
                values.append(Value(
                    attribute=attribute,
                    text=dmp_contact.get('ype')
                ))

        for set_index, dmp_dataset in enumerate(self.dmp['dataset']):
            # dmp/dataset/data_quality_assurance
            for collection_index, text in enumerate(dmp_dataset.get('data_quality_assurance', [])):
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/quality_assurance'),
                    set_index=set_index,
                    collection_index=collection_index,
                    text=text
                ))

            # dmp/dataset/dataset_id
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

            # dmp/dataset/description
            if dmp_dataset.get('description'):
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/description'),
                    set_index=set_index,
                    text=dmp_dataset.get('description')
                ))

            # dmp/dataset/issued
            if dmp_dataset.get('issued'):
                attribute = \
                    self.get_attribute(path='project/dataset/issued') or \
                    self.get_attribute(path='project/dataset/data_publication_date')

                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=dmp_dataset.get('issued')
                ))

            # dmp/dataset/keyword
            for collection_index, text in enumerate(dmp_dataset.get('keyword', [])):
                values.append(Value(
                    attribute=self.get_attribute(path='project/research_question/keywords'),
                    set_index=set_index,
                    collection_index=collection_index,
                    text=text
                ))

            # dmp/dataset/language
            if dmp_dataset.get('language'):
                attribute = self.get_attribute(path='project/dataset/language')
                option = self.get_option(self.language_options.get(self.dmp_dataset.get('language')))
                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    option=option
                ))

            # dmp/dataset/personal_data
            if dmp_dataset.get('personal_data'):
                attribute = self.get_attribute(path='project/dataset/sensitive_data/personal_data_yesno/yesno')
                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=self.yes_no.get(dmp_dataset.get('personal_data'), '0')
                ))

            # dmp/dataset/preservation_statement
            if dmp_dataset.get('preservation_statement'):
                attribute = self.get_attribute(path='project/dataset/preservation/purpose')
                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=dmp_dataset.get('preservation_statement')
                ))

            # dmp/dataset/sensitive_data
            if dmp_dataset.get('sensitive_data'):
                attribute = self.get_attribute(path='project/dataset/sensitive_data/personal_data/bdsg_3_9')
                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=self.yes_no.get(dmp_dataset.get('sensitive_data'), '0')
                ))

            # dmp/dataset/title
            if dmp_dataset.get('title'):
                attribute = self.get_attribute(path='project/dataset/title')
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/title'),
                    set_index=set_index,
                    text=dmp_dataset.get('title')
                ))
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/id'),
                    set_index=set_index,
                    text=dmp_dataset.get('title')
                ))

            # dmp/dataset/type
            if dmp_dataset.get('type'):
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/type'),
                    set_index=set_index,
                    text=dmp_dataset.get('type')
                ))

        # dmp/dataset/dataset_id
        dmp_id = self.dmp.get('dmp_id')
        if dmp_id:
            if dmp_id.get('identifier'):
                values.append(Value(
                    attribute=self.get_attribute(path='project/dmp/identifier'),
                    set_index=set_index,
                    text=dmp_id.get('identifier')
                ))
            if dmp_id.get('type'):
                values.append(Value(
                    attribute=self.get_attribute(path='project/dmp/identifier_type'),
                    set_index=set_index,
                    text=dmp_id.get('type')
                ))

        # dmp/ethical_issues_description
        if self.dmp.get('ethical_issues_description'):
            values.append(Value(
                attribute=self.get_attribute(path='project/ethical_issues/description'),
                text=self.dmp.get('ethical_issues_description')
            ))

        # dmp/ethical_issues_exist
        if self.dmp.get('ethical_issues_exist'):
            values.append(Value(
                attribute=self.get_attribute(path='project/ethical_issues/exists'),
                text=self.dmp.get('ethical_issues_exist')
            ))

        # dmp/language
        if self.dmp.get('language'):
            values.append(Value(
                attribute=self.get_attribute(path='project/language'),
                option=self.get_option(self.language_options.get(self.dmp.get('language')))
            ))

        # dmp/project
        dmp_project = self.dmp.get('project')
        if dmp_project:
            if dmp_project[0].get('start'):
                values.append(Value(
                    attribute=self.get_attribute(path='project/schedule/project_start'),
                    set_index=set_index,
                    text=dmp_project[0].get('start')
                ))
            if dmp_project[0].get('end'):
                values.append(Value(
                    attribute=self.get_attribute(path='project/schedule/project_end'),
                    set_index=set_index,
                    text=dmp_project[0].get('end')
                ))

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

    def get_option(self, path):
        try:
            return Option.objects.get(path=path)
        except Option.DoesNotExist:
            return None
