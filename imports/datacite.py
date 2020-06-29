import mimetypes

from django.utils.timezone import now

from rdmo.core.xml import get_ns_map, get_uri, read_xml_file
from rdmo.domain.models import Attribute
from rdmo.projects.imports import Import
from rdmo.projects.models import Project, Value
from rdmo.questions.models import Catalog


class DataCiteImport(Import):

    def check(self):
        file_type, encoding = mimetypes.guess_type(self.file_name)
        if file_type == 'application/xml':
            self.root = read_xml_file(self.file_name)
            if self.root:
                self.ns_map = get_ns_map(self.root)
                if self.root.tag == 'resources':
                    self.resources = self.root
                    return True
                elif self.root.tag == 'resource':
                    self.resources = [self.root]
                    return True

    def process(self):
        project = Project()

        project.title = 'Test'
        project.description = 'Test'
        project.created = now()
        project.catalog = Catalog.objects.first()

        values = []

        # identifier
        for set_index, resource in enumerate(self.resources):
            if resource.find('./identifier') is not None:
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/identifier'),
                    set_index=set_index,
                    text=resource.find('./identifier').text
                ))
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/identifier_type'),
                    set_index=set_index,
                    text=resource.find('./identifier').attrib.get('identifierType', 'DOI')
                ))

            # creators
            if resource.find('./creators/creator/creatorName') is not None:
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/creator/name'),
                    set_index=set_index,
                    text=resource.find('./creators/creator/creatorName').text
                ))

            # title
            if resource.find('./titles/title') is not None:
                attribute = \
                    self.get_attribute(path='project/dataset/title') or \
                    self.get_attribute(path='project/dataset/id')
                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=resource.find('./titles/title').text
                ))

            # publisher
            if resource.find('./publisher') is not None:
                attribute = \
                    self.get_attribute(path='project/dataset/publisher') or \
                    self.get_attribute(path='project/dataset/preservation/repository')
                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=resource.find('./publisher').text
                ))

            # publicationYear
            if resource.find('./publicationYear') is not None:
                attribute = \
                    self.get_attribute(path='project/dataset/issued') or \
                    self.get_attribute(path='project/dataset/data_publication_date')
                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=resource.find('./publicationYear').text
                ))

            # subjects
            if resource.find('./subjects/subject') is not None:
                attribute = \
                    self.get_attribute(path='project/dataset/research/subject') or \
                    self.get_attribute(path='project/research_field/title')
                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=resource.find('./subjects/subject').text
                ))

            # dates
            if resource.find('./created') is not None:
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/created'),
                    set_index=set_index,
                    text=resource.find('./dates/issued').text
                ))
            if resource.find('./dates/issued') is not None:
                attribute = \
                    self.get_attribute(path='project/dataset/issued') or \
                    self.get_attribute(path='project/dataset/data_publication_date')
                values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=resource.find('./dates/issued').text
                ))

            # language
            if resource.find('./language') is not None:
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/language'),
                    set_index=set_index,
                    text=resource.find('./language').text
                ))

            # resourceType and resourceTypeGeneral
            if resource.find('./resourceType') is not None:
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/resource_type'),
                    set_index=set_index,
                    text=resource.find('./resourceType').text
                ))
                if resource.find('./resourceType').attrib.get('resourceTypeGeneral') is not None:
                    values.append(Value(
                        attribute=self.get_attribute(path='project/dataset/resource_type_general'),
                        set_index=set_index,
                        text=resource.find('./resourceType').attrib.get('resourceTypeGeneral', 'Dataset')
                    ))

            # rightsList/rights
            if resource.find('./rightsList/rights') is not None:
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/sharing/conditions'),
                    set_index=set_index,
                    text=resource.find('./rightsList/rights').text
                ))

            # descriptions/description
            if resource.find('./descriptions/description') is not None:
                values.append(Value(
                    attribute=self.get_attribute(path='project/dataset/description'),
                    set_index=set_index,
                    text=resource.find('./descriptions/description').text
                ))

        # snapshots, tasks, and views are not part of DataCite
        snapshots = []
        tasks = []
        views = []

        return project, values, snapshots, tasks, views

    def get_attribute(self, path):
        try:
            return Attribute.objects.get(path=path)
        except Attribute.DoesNotExist:
            return None
