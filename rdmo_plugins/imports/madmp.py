import json
import mimetypes

from rdmo.projects.imports import Import
from rdmo.projects.models import Project, Value
from rdmo.questions.models import Catalog


class MaDMPImport(Import):

    yes_no = {
        'yes': '1',
        'no': '0',
        'unknown': '0'
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
            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                return False

            if self.dmp:
                return True

    def process(self):
        if self.current_project is None:
            self.catalog = Catalog.objects.first()

            self.project = Project()
            self.project.title = self.dmp.get('title')
            self.project.description = self.dmp.get('description', '')
            self.project.created = self.dmp.get('created', '')
            self.project.catalog = self.catalog
        else:
            self.catalog = self.current_project.catalog

        dmp_contact = self.dmp.get('contact')
        if dmp_contact:
            if dmp_contact.get('name'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dmp/contact/name'),
                    text=dmp_contact.get('name')
                ))
            if dmp_contact.get('mbox'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dmp/contact/mbox'),
                    text=dmp_contact.get('mbox')
                ))
            dmp_contact_id = dmp_contact.get('contact_id')
            if dmp_contact_id.get('identifier'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dmp/contact/identifier'),
                    text=dmp_contact.get('identifier')
                ))
            if dmp_contact_id.get('type'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dmp/contact/identifier_type'),
                    text=dmp_contact.get('ype')
                ))

        for set_index, dmp_dataset in enumerate(self.dmp['dataset']):
            # dmp/dataset/data_quality_assurance
            for collection_index, text in enumerate(dmp_dataset.get('data_quality_assurance', [])):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/quality_assurance'),
                    set_index=set_index,
                    collection_index=collection_index,
                    text=text
                ))

            # dmp/dataset/dataset_id
            dmp_dataset_id = dmp_dataset.get('dataset_id')
            if dmp_dataset_id:
                if dmp_dataset_id.get('identifier'):
                    self.values.append(Value(
                        attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/identifier'),
                        set_index=set_index,
                        text=dmp_dataset_id.get('identifier')
                    ))
                if dmp_dataset_id.get('type'):
                    self.values.append(Value(
                        attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/identifier_type'),
                        set_index=set_index,
                        text=dmp_dataset_id.get('type')
                    ))

            # dmp/dataset/description
            if dmp_dataset.get('description'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/description'),
                    set_index=set_index,
                    text=dmp_dataset.get('description')
                ))

            # dmp/dataset/issued
            if dmp_dataset.get('issued'):
                attribute = \
                    self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/issued') or \
                    self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/data_publication_date')

                self.values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=dmp_dataset.get('issued')
                ))

            # dmp/dataset/keyword
            for collection_index, text in enumerate(dmp_dataset.get('keyword', [])):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/research_question/keywords'),
                    set_index=set_index,
                    collection_index=collection_index,
                    text=text
                ))

            # dmp/dataset/language
            if dmp_dataset.get('language'):
                attribute = self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/language')
                option = self.get_option(self.language_options.get(self.dmp_dataset.get('language')))
                self.values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    option=option
                ))

            # dmp/dataset/personal_data
            if dmp_dataset.get('personal_data'):
                attribute = self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/sensitive_data/personal_data_yesno/yesno')
                self.values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=self.yes_no.get(dmp_dataset.get('personal_data'), '0')
                ))

            # dmp/dataset/preservation_statement
            if dmp_dataset.get('preservation_statement'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/preservation/purpose'),
                    set_index=set_index,
                    text=dmp_dataset.get('preservation_statement')
                ))

            # dmp/dataset/sensitive_data
            if dmp_dataset.get('sensitive_data'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/sensitive_data/personal_data/bdsg_3_9'),
                    set_index=set_index,
                    text=self.yes_no.get(dmp_dataset.get('sensitive_data'), '0')
                ))

            # dmp/dataset/title
            if dmp_dataset.get('title'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/title'),
                    set_index=set_index,
                    text=dmp_dataset.get('title')
                ))
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/id'),
                    set_index=set_index,
                    text=dmp_dataset.get('title')
                ))

            # dmp/dataset/type
            if dmp_dataset.get('type'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/type'),
                    set_index=set_index,
                    text=dmp_dataset.get('type')
                ))

        # dmp/dataset/dataset_id
        dmp_id = self.dmp.get('dmp_id')
        if dmp_id:
            if dmp_id.get('identifier'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dmp/identifier'),
                    set_index=set_index,
                    text=dmp_id.get('identifier')
                ))
            if dmp_id.get('type'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dmp/identifier_type'),
                    set_index=set_index,
                    text=dmp_id.get('type')
                ))

        # dmp/ethical_issues_description
        if self.dmp.get('ethical_issues_description'):
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/ethical_issues/description'),
                text=self.dmp.get('ethical_issues_description')
            ))

        # dmp/ethical_issues_exist
        if self.dmp.get('ethical_issues_exist'):
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/ethical_issues/exists'),
                text=self.dmp.get('ethical_issues_exist')
            ))

        # dmp/language
        if self.dmp.get('language'):
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/language'),
                option=self.get_option(self.language_options.get(self.dmp.get('language')))
            ))

        # dmp/project
        dmp_project = self.dmp.get('project')
        if dmp_project:
            if dmp_project[0].get('start'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/schedule/project_start'),
                    set_index=set_index,
                    text=dmp_project[0].get('start')
                ))
            if dmp_project[0].get('end'):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/schedule/project_end'),
                    set_index=set_index,
                    text=dmp_project[0].get('end')
                ))
