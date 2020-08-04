import mimetypes

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rdmo.core.xml import get_ns_map, read_xml_file
from rdmo.domain.models import Attribute
from rdmo.projects.imports import Import
from rdmo.projects.models import Value


class DataCiteImport(Import):

    def check(self):
        file_type, encoding = mimetypes.guess_type(self.file_name)
        if file_type == 'application/xml':
            self.root = read_xml_file(self.file_name)
            if self.root:
                self.ns_map = get_ns_map(self.root)
                if self.root.tag == '{{{ns0}}}resource'.format(**self.ns_map):
                    return True

    def process(self):
        if self.current_project is None:
            raise ValidationError(_('DataCite files can only be imported into existing projects. Please create a project first.'))

        self.catalog = self.current_project.catalog

        # get existing datasets
        current_datasets = self.current_project.values.filter(
            snapshot=None,
            attribute__path='project/dataset/id'
        )

        # get maximum set_index to only append datasets
        try:
            set_index = max([d.set_index for d in current_datasets]) + 1
        except ValueError:
            set_index = 0

        # identifier
        identifier_node = self.root.find('./ns0:identifier', self.ns_map)
        if identifier_node is not None:
            self.values.append(self.get_value(
                attribute=self.get_attribute(path='project/dataset/identifier'),
                set_index=set_index,
                text=identifier_node.text
            ))

            # identifierType
            self.values.append(self.get_value(
                attribute=self.get_attribute(path='project/dataset/identifier_type'),
                set_index=set_index,
                text=identifier_node.attrib.get('identifierType', 'DOI')
            ))

        # first creator name
        creator_node = self.root.find('./ns0:creators/ns0:creator/ns0:creatorName', self.ns_map)
        if creator_node is not None:
            self.values.append(self.get_value(
                attribute=self.get_attribute(path='project/dataset/creator/name'),
                set_index=set_index,
                text=creator_node.text
            ))

        # title
        title_node = self.root.find('./ns0:titles/ns0:title', self.ns_map)
        if title_node is not None:
            attribute = self.get_attribute(path='project/dataset/id')
            self.values.append(self.get_value(
                attribute=attribute,
                set_index=set_index,
                text=title_node.text
            ))

        # publisher
        publisher_node = self.root.find('./ns0:publisher', self.ns_map)
        if publisher_node is not None:
            attribute = \
                self.get_attribute(path='project/dataset/publisher') or \
                self.get_attribute(path='project/dataset/preservation/repository')
            self.values.append(self.get_value(
                attribute=attribute,
                set_index=set_index,
                text=publisher_node.text
            ))

        # subjects
        subject_nodes = self.root.find('./ns0:subjects/ns0:subject', self.ns_map)
        for collection_index, subject_node in enumerate(subject_nodes):
            if subject_node is not None:
                attribute = self.get_attribute(path='project/dataset/subject')
                self.values.append(self.get_value(
                    attribute=attribute,
                    set_index=set_index,
                    collection_index=collection_index,
                    text=subject_node.text
                ))

        # dates
        created_node = self.root.find("./ns0:dates/ns0:date[@dateType='Created']", self.ns_map)
        if created_node is not None:
            attribute = self.get_attribute(path='project/dataset/created')
            self.values.append(self.get_value(
                attribute=attribute,
                set_index=set_index,
                text=created_node.text
            ))
        issued_node = self.root.find("./ns0:dates/ns0:date[@dateType='Issued']", self.ns_map)
        if issued_node is not None:
            attribute = \
                self.get_attribute(path='project/dataset/issued') or \
                self.get_attribute(path='project/dataset/data_publication_date')
            self.values.append(self.get_value(
                attribute=attribute,
                set_index=set_index,
                text=issued_node.text
            ))
        else:
            publication_year_node = self.root.find('./ns0:publicationYear', self.ns_map)
            if publication_year_node is not None:
                attribute = \
                    self.get_attribute(path='project/dataset/issued') or \
                    self.get_attribute(path='project/dataset/data_publication_date')
                self.values.append(self.get_value(
                    attribute=attribute,
                    set_index=set_index,
                    text=publication_year_node.text
                ))

        # language
        language_node = self.root.find('./ns0:language', self.ns_map)
        if language_node is not None:
            self.values.append(self.get_value(
                attribute=self.get_attribute(path='project/dataset/language'),
                set_index=set_index,
                text=language_node.text
            ))

        # resourceType
        resource_type_node = self.root.find('./ns0:resourceType', self.ns_map)
        if resource_type_node is not None:
            self.values.append(self.get_value(
                attribute=self.get_attribute(path='project/dataset/resource_type'),
                set_index=set_index,
                text=resource_type_node.text
            ))

            # resourceTypeGeneral
            self.values.append(self.get_value(
                attribute=self.get_attribute(path='project/dataset/resource_type_general'),
                set_index=set_index,
                text=resource_type_node.attrib.get('resourceTypeGeneral', 'Dataset')
            ))

        # descriptions/description
        description_node = self.root.find("./ns0:descriptions/ns0:description[@descriptionType='Abstract']", self.ns_map)
        if description_node is not None:
            self.values.append(self.get_value(
                attribute=self.get_attribute(path='project/dataset/description'),
                set_index=set_index,
                text=description_node.text
            ))

    def get_attribute(self, path):
        try:
            return Attribute.objects.get(path=path)
        except Attribute.DoesNotExist:
            return None

    def get_value(self, **kwargs):
        value = Value(**kwargs)
        return {
            'value': value,
            'question': value.get_question(self.catalog),
            'current': value.get_current_value(self.current_project)
        }
