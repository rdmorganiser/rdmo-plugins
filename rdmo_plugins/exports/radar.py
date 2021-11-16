import logging
import time
import zipfile

from collections import defaultdict

from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, reverse, render
from django.utils.translation import gettext_lazy as _

from rdmo.core.exports import prettify_xml
from rdmo.core.renderers import BaseXMLRenderer
from rdmo.projects.exports import Export
from rdmo.services.providers import OauthProviderMixin

logger = logging.getLogger(__name__)


class RadarMixin(object):

    identifier_type_options = {
        'identifier_type/doi': 'DOI',
        'identifier_type/handle': 'HANDLE',
        'identifier_type/other': 'OTHER'
    }

    language_options = {
        'language/en': 'eng',
        'language/de': 'deu'
    }

    name_type_options = {
        'name_type/personal': 'Personal',
        'name_type/organizational': 'Organizational'
    }

    name_identifier_scheme_options = {
        'name_identifier_scheme/orcid': 'ORCID',
        'name_identifier_scheme/insi': 'INSI',
        'name_identifier_scheme/ror': 'ROR',
        'name_identifier_scheme/grid': 'GRID'
    }

    contributor_type_options = {
        'contributor_type/contact_persion': 'ContactPerson',
        'contributor_type/data_collector': 'DataCollector',
        'contributor_type/data_curator': 'DataCurator',
        'contributor_type/data_manager': 'DataManager',
        'contributor_type/distributor': 'Distributor',
        'contributor_type/editor': 'Editor',
        'contributor_type/hosting_institution': 'HostingInstitution',
        'contributor_type/producer': 'Producer',
        'contributor_type/project_leader': 'ProjectLeader',
        'contributor_type/project_manager': 'ProjectManager',
        'contributor_type/project_member': 'ProjectMember',
        'contributor_type/registration_agency': 'RegistrationAgency',
        'contributor_type/registration_authority': 'RegistrationAuthority',
        'contributor_type/related_person': 'RelatedPerson',
        'contributor_type/researcher': 'Researcher',
        'contributor_type/research_group': 'ResearchGroup',
        'contributor_type/rights_holder': 'RightsHolder',
        'contributor_type/sponsor': 'Sponsor',
        'contributor_type/supervisor': 'Supervisor',
        'contributor_type/work_package_leader': 'WorkPackageLeader',
        'contributor_type/other': 'Other'
    }

    resource_type_options = {
        'resource_type_general/audiovisual': 'Audiovisual',
        'resource_type_general/collection': 'Collection',
        'resource_type_general/data_paper': 'DataPaper',
        'resource_type_general/dataset': 'Dataset',
        'resource_type_general/event': 'Event',
        'resource_type_general/image': 'Image',
        'resource_type_general/interactive_resource': 'InteractiveResource',
        'resource_type_general/model': 'Model',
        'resource_type_general/physical_object': 'PhysicalObject',
        'resource_type_general/service': 'Service',
        'resource_type_general/software': 'Software',
        'resource_type_general/sound': 'Sound',
        'resource_type_general/text': 'Text',
        'resource_type_general/workflow': 'Workflow',
        'resource_type_general/other': 'Other'
    }

    controlled_subject_area_options = {
        'radar_controlled_subject_area/agriculture': 'Agriculture',
        'radar_controlled_subject_area/architecture': 'Architecture',
        'radar_controlled_subject_area/arts_and_media': 'Arts and Media',
        'radar_controlled_subject_area/astrophysics_and_astronomy': 'Astrophysics and Astronomy',
        'radar_controlled_subject_area/biochemistry': 'Biochemistry',
        'radar_controlled_subject_area/biology': 'Biology',
        'radar_controlled_subject_area/behavioural_sciences': 'Behavioural Sciences',
        'radar_controlled_subject_area/chemistry': 'Chemistry',
        'radar_controlled_subject_area/computer_science': 'Computer Science',
        'radar_controlled_subject_area/economics': 'Economics',
        'radar_controlled_subject_area/engineering': 'Engineering',
        'radar_controlled_subject_area/environmental_science_and_ecology': 'Environmental Science and Ecology',
        'radar_controlled_subject_area/ethnology': 'Ethnology',
        'radar_controlled_subject_area/geological_science': 'Geological Science',
        'radar_controlled_subject_area/geography': 'Geography',
        'radar_controlled_subject_area/history': 'History',
        'radar_controlled_subject_area/horticulture': 'Horticulture',
        'radar_controlled_subject_area/information_technology': 'Information Technology',
        'radar_controlled_subject_area/life_science': 'Life Science',
        'radar_controlled_subject_area/linguistics': 'Linguistics',
        'radar_controlled_subject_area/materials_science': 'Materials Science',
        'radar_controlled_subject_area/mathematics': 'Mathematics',
        'radar_controlled_subject_area/medicine': 'Medicine',
        'radar_controlled_subject_area/philosophy': 'Philosophy',
        'radar_controlled_subject_area/physics': 'Physics',
        'radar_controlled_subject_area/psychology': 'Psychology',
        'radar_controlled_subject_area/social_sciences': 'Social Sciences',
        'radar_controlled_subject_area/software_technology': 'Software Technology',
        'radar_controlled_subject_area/sports': 'Sports',
        'radar_controlled_subject_area/theology': 'Theology',
        'radar_controlled_subject_area/veterinary_medicine': 'Veterinary Medicine',
        'radar_controlled_subject_area/other': 'Other'
    }

    data_source_options = {
        'radar_data_source/instrument': 'Instrument',
        'radar_data_source/media': 'Media',
        'radar_data_source/observation': 'Observation',
        'radar_data_source/trial': 'Trial',
        'radar_data_source/organism': 'Organism',
        'radar_data_source/tissue': 'Tissue',
        'radar_data_source/other': 'Other'
    }

    software_type_options = {
        'radar_software_type/resource_production': 'Resource Production',
        'radar_software_type/resource_processing': 'Resource Processing',
        'radar_software_type/resource_viewing': 'Resource Viewing',
        'radar_software_type/other': 'Other'
    }

    controlled_rights_options = {
        'dataset_license_types/71': 'CC BY 4.0 Attribution',
        'dataset_license_types/74': 'CC BY-ND 4.0 Attribution-NoDerivs',
        'dataset_license_types/75': 'CC BY-SA 4.0 Attribution-ShareAlike',
        'dataset_license_types/73': 'CC BY-NC 4.0 Attribution-NonCommercial',
        # '': 'CC BY-NC-SA 4.0 Attribution-NonCommercial-ShareAlike',
        # '': 'CC BY-NC-ND 4.0 Attribution-NonCommercial-NoDerivs',
        'dataset_license_types/cc0': 'CC0 1.0 Universal Public Domain Dedication',
        # '': 'All rights reserved',
        'dataset_license_types/233': 'Other'
    }

    relation_type_options = {
        'relation_type/is_cited_by': 'IsCitedBy',
        'relation_type/cites': 'Cites',
        'relation_type/is_supplement_to': 'IsSupplementTo',
        'relation_type/is_supplemented_by': 'IsSupplementedBy',
        'relation_type/is_continued_by': 'IsContinuedBy',
        'relation_type/continues': 'Continues',
        'relation_type/describes': 'Describes',
        'relation_type/is_described_by': 'IsDescribedBy',
        'relation_type/has_metadata': 'HasMetadata',
        'relation_type/is_metadata_for': 'IsMetadataFor',
        'relation_type/has_version': 'HasVersion',
        'relation_type/is_version_of': 'IsVersionOf',
        'relation_type/is_new_version_of': 'IsNewVersionOf',
        'relation_type/is_previous_version_of': 'IsPreviousVersionOf',
        'relation_type/is_part_of': 'IsPartOf',
        'relation_type/has_part': 'HasPart',
        'relation_type/is_published_in': 'IsPublishedIn',
        'relation_type/is_referenced_by': 'IsReferencedBy',
        'relation_type/references': 'References',
        'relation_type/is_documented_by': 'IsDocumentedBy',
        'relation_type/documents': 'Documents',
        'relation_type/is_compiled_by': 'IsCompiledBy',
        'relation_type/Compiles': 'Compiles',
        'relation_type/is_variant_form_of': 'IsVariantFormOf',
        'relation_type/is_original_form_of': 'IsOriginalFormOf',
        'relation_type/is_identical_to': 'IsIdenticalTo',
        'relation_type/is_reviewed_by': 'IsReviewedBy',
        'relation_type/reviews': 'Reviews',
        'relation_type/is_derived_from': 'IsDerivedFrom',
        'relation_type/is_source_of': 'IsSourceOf',
        'relation_type/is_required_by': 'IsRequiredBy',
        'relation_type/requires': 'Requires',
        'relation_type/obsoletes': 'Obsoletes',
        'relation_type/is_obsoleted_by': 'IsObsoletedBy'
    }

    def get_datasets(self):
        datasets = []
        for rdmo_dataset in self.get_set('project/dataset/id'):
            set_index = rdmo_dataset.set_index
            dataset = self.get_dataset(set_index)
            datasets.append(dataset)

        return datasets

    def get_dataset(self, set_index):
        dataset = defaultdict(list)

        # file_name
        dataset['file_name'] = '{}.xml'.format(
            self.get_text('project/dataset/identifier', set_index=set_index) or
            self.get_text('project/dataset/id', set_index=set_index) or
            str(set_index + 1)
        )

        # identifier
        identifier = self.get_text('project/dataset/identifier', set_index=set_index)
        if identifier:
            dataset['identifier'] = identifier
            dataset['identifierType'] = \
                self.get_option(self.identifier_type_options, 'project/dataset/identifier_type', set_index=set_index) or \
                self.get_option(self.identifier_type_options, 'project/dataset/pids/system', set_index=set_index) or \
                'OTHER'
        else:
            dataset['identifier'] = self.get_text('project/dataset/id', set_index=set_index)
            dataset['identifierType'] = 'OTHER'

        # creators
        for creator_set in self.get_set('project/dataset/creator/name', set_prefix=str(set_index)):
            creator = self.get_name('project/dataset/creator',
                                    set_prefix=creator_set.set_prefix, set_index=creator_set.set_index)
            if creator:
                dataset['creators'].append(creator)

        # title
        dataset['title'] =  \
            self.get_text('project/dataset/title', set_index=set_index) or \
            self.get_text('project/dataset/id', set_index=set_index) or \
            'Dataset #{}'.format(set_index + 1)

        # publisher
        publisher = \
            self.get_text('project/dataset/publisher', set_index=set_index) or \
            self.get_text('project/dataset/preservation/repository', set_index=set_index)
        if publisher:
            dataset['publisher'] = publisher

        # productionYear
        dataset['productionYear'] = \
            self.get_year('project/dataset/created', set_index=set_index) or \
            self.get_year('project/dataset/data_publication_date', set_index=set_index)

        # publicationYear
        dataset['publicationYear'] = \
            self.get_year('project/dataset/issued', set_index=set_index) or \
            self.get_year('project/dataset/data_publication_date', set_index=set_index)

        # subjectArea
        subject_areas = \
            self.get_values('project/dataset/subject', set_index=set_index) or \
            self.get_values('project/research_field/title', set_index=set_index)

        if subject_areas:
            dataset['subjectAreas'] = []
            for subject_area in subject_areas:
                if subject_area.is_true:
                    if subject_area.option:
                        controlled_subject_area_name = self.controlled_subject_area_options.get(subject_area.option.path, 'Other')
                    else:
                        controlled_subject_area_name = 'Other'

                    if controlled_subject_area_name == 'Other':
                        dataset['subjectAreas'].append({
                            'controlledSubjectAreaName': controlled_subject_area_name,
                            'additionalSubjectAreaName': subject_area.value
                        })
                    else:
                        dataset['subjectAreas'].append({
                            'controlledSubjectAreaName': controlled_subject_area_name
                        })

        # resource
        resource_type = self.get_text('project/dataset/resource_type', set_index=set_index)
        if resource_type:
            dataset['resourceType'] = resource_type
            dataset['resourceTypeGeneral'] = \
                self.get_option(self.resource_type_options, 'project/dataset/resource_type_general', set_index=set_index)

        dataset['title'] = \
            self.get_text('project/dataset/title', set_index=set_index) or \
            self.get_text('project/dataset/id', set_index=set_index) or \
            'Dataset #{}'.format(set_index + 1)

        # alternate_identifiers
        for alternate_identifier_set in self.get_set('project/dataset/alternate_identifier/identifier', set_prefix=str(set_index)):
            dataset['alternateIdentifiers'].append({
                'alternateIdentifier': self.get_text('project/dataset/alternate_identifier/identifier',
                                                     set_prefix=alternate_identifier_set.set_prefix,
                                                     set_index=alternate_identifier_set.set_index),
                'alternateIdentifierType': self.get_option(self.identifier_type_options,
                                                           'project/dataset/alternate_identifier/identifier_type',
                                                           set_prefix=alternate_identifier_set.set_prefix,
                                                           set_index=alternate_identifier_set.set_index)
            })

        # related_identifiers
        for related_identifier_set in self.get_set('project/dataset/related_identifier/identifier', set_prefix=str(set_index)):
            dataset['relatedIdentifiers'].append({
                'relatedIdentifier': self.get_text('project/dataset/related_identifier/identifier',
                                                   set_prefix=related_identifier_set.set_prefix,
                                                   set_index=related_identifier_set.set_index),
                'relatedIdentifierType': self.get_option(self.identifier_type_options,
                                                         'project/dataset/related_identifier/identifier_type',
                                                         set_prefix=related_identifier_set.set_prefix,
                                                         set_index=related_identifier_set.set_index),
                'relationType': self.get_option(self.relation_type_options,
                                                'project/dataset/related_identifier/relation_type',
                                                set_prefix=related_identifier_set.set_prefix,
                                                set_index=related_identifier_set.set_index)
            })

        # rights
        rights_list = self.get_values('project/dataset/sharing/conditions', set_index=set_index)
        if rights_list:
            dataset['rights'] = []
            for rights in rights_list:
                if rights.option:
                    controlled_rights = self.controlled_rights_options.get(rights.option.path, 'Other')
                else:
                    controlled_rights = 'Other'

                dataset['rights'].append({
                    'controlledRights': controlled_rights,
                    'additionalRights': rights.value if controlled_rights == 'Other' else None
                })

        # rights holders
        rights_holders = self.get_list('project/dataset/sharing/rights_holder', set_index=set_index)
        if rights_holders:
            dataset['rightsHolders'] = rights_holders

        # description
        description = self.get_text('project/dataset/description', set_index=set_index)
        if description:
            dataset['descriptions'] = [{
                'description': description,
                'descriptionType': 'Abstract'
            }]

        # keywords
        keywords = self.get_list('project/research_question/keywords')
        if keywords:
            dataset['keywords'] = keywords

        # contributors
        for contributor_set in self.get_set('project/dataset/contributor/name', set_prefix=str(set_index)):
            contributor = self.get_name('project/dataset/contributor',
                                        set_prefix=contributor_set.set_prefix, set_index=contributor_set.set_index)
            if contributor:
                dataset['contributors'].append(contributor)

        # language
        dataset['language'] = self.get_option(self.language_options, 'project/dataset/language', set_index=set_index)

        # dataSource
        data_source = self.get_text('project/dataset/data_source', set_index=set_index)
        if data_source:
            dataset['dataSources'] = [{
                'dataSource': data_source,
                'dataSourceDetail': self.get_option(self.data_source_options, 'project/dataset/data_source_detail', set_index=set_index)
            }]

        # dataProcessing
        data_processing = self.get_list('project/dataset/data_processing', set_index=set_index)
        if data_processing:
            dataset['dataProcessing'] = data_processing

        # funding_references
        for funder in self.get_set('project/funder/id'):
            dataset['fundingReferences'].append({
                'funderName': self.get_text('project/funder/name', set_index=funder.set_index),
                'funderIdentifier': self.get_text('project/funder/name_identifier', set_index=funder.set_index),
                'funderIdentifierType': self.get_option(self.name_identifier_scheme_options, 'project/funder/name_identifier_scheme', set_index=funder.set_index),
                'awardURI': self.get_text('project/funder/programme/url', set_index=funder.set_index),
                'awardNumber': self.get_text('project/funder/programme/number', set_index=funder.set_index),
                'awardTitle': self.get_text('project/funder/programme/title', set_index=funder.set_index)
            })

        return dataset

    def get_name(self, attribute, set_prefix='', set_index=0):
        name_text = self.get_text(attribute + '/name', set_prefix=set_prefix, set_index=set_index)
        if name_text:
            name = {
                'name': name_text,
                'nameType': self.get_option(self.name_type_options, attribute + '/name_type',
                                            set_prefix=set_prefix, set_index=set_index, default='Personal'),
            }

            # contributor_name
            contributor_type = self.get_option(self.contributor_type_options, attribute + '/contributor_type',
                                               set_prefix=set_prefix, set_index=set_index, default='Other')
            if contributor_type:
                name['contributorType'] = contributor_type

            # given_name
            given_name = self.get_text(attribute + '/given_name', set_prefix=set_prefix, set_index=set_index)
            if given_name:
                name['givenName'] = given_name

            # family_name
            family_name = self.get_text(attribute + '/family_name', set_prefix=set_prefix, set_index=set_index)
            if family_name:
                name['familyName'] = family_name

            # identifier
            identifier = self.get_text(attribute + '/name_identifier', set_prefix=set_prefix, set_index=set_index)
            if identifier:
                name['nameIdentifier'] = identifier
                name['nameIdentifierScheme'] = self.get_option(self.name_identifier_scheme_options,
                                                               attribute + '/name_identifier_scheme',
                                                               set_prefix=set_prefix, set_index=set_index,
                                                               default='ORCID')

            # affiliations
            affiliations = self.get_list(attribute + '/affiliation', set_prefix=set_prefix, set_index=set_index)
            if affiliations:
                name['affiliations'] = []
                for affiliation in affiliations:
                    name['affiliations'].append({
                        'affiliation': affiliation
                    })

            return name
        else:
            return None


class RadarExport(RadarMixin, Export):

    class Renderer(BaseXMLRenderer):

        scheme_uri = {
            'INSI': 'http://www.isni.org/',
            'ORCID': 'https://orcid.org',
            'ROR': 'https://ror.org/',
            'GRID': 'https://www.grid.ac/'
        }

        def render_document(self, xml, dataset):
            xml.startElement('ns2:radarDataset', {
                'xmlns': 'http://radar-service.eu/schemas/descriptive/radar/v09/radar-elements',
                'xmlns:ns2': 'http://radar-service.eu/schemas/descriptive/radar/v09/radar-dataset'
            })

            # identifier
            identifier = dataset.get('identifier')
            if identifier:
                self.render_text_element(xml, 'identifier', {
                    'identifierType': dataset.get('identifierType', 'OTHER')
                }, identifier)

            # creators
            creators = dataset.get('creators')
            if creators:
                xml.startElement('creators', {})
                for creator in creators:
                    xml.startElement('creator', {})
                    self.render_text_element(xml, 'creatorName', {
                        'nameType': creator.get('nameType')
                    }, creator.get('name'))

                    if creator.get('givenName'):
                        self.render_text_element(xml, 'givenName', {}, creator.get('givenName'))

                    if creator.get('familyName'):
                        self.render_text_element(xml, 'familyName', {}, creator.get('familyName'))

                    if creator.get('nameIdentifier'):
                        self.render_text_element(xml, 'nameIdentifier', {
                            'nameIdentifierScheme': creator.get('nameIdentifierScheme'),
                            'schemeURI': self.scheme_uri.get(creator.get('schemeURI')),
                        }, creator.get('nameIdentifier'))

                    for affiliation in creator.get('affiliations', []):
                        self.render_text_element(xml, 'affiliation', {
                            'affiliationIdentifier': affiliation.get('affiliationIdentifier'),
                            'affiliationIdentifierScheme': affiliation.get('affiliationIdentifierScheme')
                        }, affiliation.get('affiliation'))

                    xml.endElement('creator')
                xml.endElement('creators')

            # title
            title = dataset.get('title')
            if title:
                self.render_text_element(xml, 'title', {}, title)

            # publisher
            publisher = dataset.get('publisher')
            if publisher:
                self.render_text_element(xml, 'publisher', {}, publisher)

            # productionYear
            production_year = dataset.get('productionYear')
            if production_year:
                self.render_text_element(xml, 'productionYear', {}, production_year)

            # publicationYear
            publication_year = dataset.get('publicationYear')
            if publication_year:
                self.render_text_element(xml, 'publicationYear', {}, publication_year)

            # subjectArea
            subject_areas = dataset.get('subjectAreas')
            if subject_areas:
                xml.startElement('subjectAreas', {})
                for subject_area in subject_areas:
                    xml.startElement('subjectArea', {})
                    self.render_text_element(xml, 'controlledSubjectAreaName', {}, subject_area.get('controlledSubjectAreaName'))
                    if subject_area.get('additionalSubjectAreaName'):
                        self.render_text_element(xml, 'additionalSubjectAreaName', {}, subject_area.get('additionalSubjectAreaName'))
                    xml.endElement('subjectArea')
                xml.endElement('subjectAreas')

            # resource
            resource = dataset.get('resource')
            if resource:
                if dataset.get('resource'):
                    self.render_text_element(xml, 'resource', {
                        'resourceType': dataset.get('resourceType')
                    }, resource)

            # rights
            rights_list = dataset.get('rights')
            if rights_list:
                xml.startElement('rights', {})
                for rights in rights_list:
                    self.render_text_element(xml, 'controlledRights', {}, rights.get('controlledRights'))

                    additional_rights = rights.get('additionalRights')
                    if additional_rights:
                        self.render_text_element(xml, 'additionalRights', {}, additional_rights)
                xml.endElement('rights')

            # rightsHolders
            rights_holders = dataset.get('rightsHolders')
            if rights_holders:
                xml.startElement('rightsHolders', {})
                for rights_holder in rights_holders:
                    self.render_text_element(xml, 'rightsHolder', {}, rights_holder)
                xml.endElement('rightsHolders')

            # additionalTitles
            additional_titles = dataset.get('additionalTitles')
            if additional_titles:
                xml.startElement('additionalTitles', {})
                for additional_title in additional_titles:
                    self.render_text_element(xml, 'additionalTitle', {
                        'additionalTitleType': additional_title['additionalTitleType']
                    }, additional_title['additionalTitle'])
                xml.endElement('additionalTitles')

            # descriptions
            descriptions = dataset.get('descriptions')
            if descriptions:
                xml.startElement('descriptions', {})
                for description in descriptions:
                    self.render_text_element(xml, 'description', {
                        'descriptionType': description.get('descriptionType', 'Abstract')
                    }, description.get('description'))
                xml.endElement('descriptions')

            # keywords
            keywords = dataset.get('keywords')
            if keywords:
                xml.startElement('keywords', {})
                for keyword in keywords:
                    self.render_text_element(xml, 'keyword', {}, keyword)
                xml.endElement('keywords')

            # contributors
            contributors = dataset.get('contributors')
            if contributors:
                xml.startElement('contributors', {})
                for contributor in dataset.get('contributors', []):
                    xml.startElement('contributor', {})
                    self.render_text_element(xml, 'contributorName', {
                        'nameType': contributor.get('nameType')
                    }, contributor.get('name'))

                    if contributor.get('givenName'):
                        self.render_text_element(xml, 'givenName', {}, contributor.get('givenName'))

                    if contributor.get('familyName'):
                        self.render_text_element(xml, 'familyName', {}, contributor.get('familyName'))

                    if contributor.get('nameIdentifier'):
                        self.render_text_element(xml, 'nameIdentifier', {
                            'nameIdentifierScheme': contributor.get('nameIdentifierScheme'),
                            'schemeURI': self.scheme_uri.get(contributor.get('schemeURI')),
                        }, contributor.get('nameIdentifier'))

                    for affiliation in contributor.get('affiliations', []):
                        self.render_text_element(xml, 'affiliation', {
                            'affiliationIdentifier': affiliation.get('affiliationIdentifier'),
                            'affiliationIdentifierScheme': affiliation.get('affiliationIdentifierScheme')
                        }, affiliation.get('affiliation'))

                    xml.endElement('contributor')
                xml.endElement('contributors')

            # language
            language = dataset.get('language')
            if language:
                self.render_text_element(xml, 'language', {}, language)

            # resource_type
            resource_type = dataset.get('resourceType')
            if resource_type:
                self.render_text_element(xml, 'resourceType', {
                    'resourceTypeGeneral': dataset.get('resourceTypeGeneral')
                }, resource_type)

            # alternate_identifiers
            alternate_identifiers = dataset.get('alternateIdentifiers')
            if alternate_identifiers:
                xml.startElement('alternateIdentifiers', {})
                for alternate_identifier in alternate_identifiers:
                    self.render_text_element(xml, 'alternateIdentifier', {
                        'alternateIdentifierType': alternate_identifier.get('alternateIdentifierType')
                    }, alternate_identifier.get('alternateIdentifier'))
                xml.endElement('alternateIdentifiers')

            # related_identifiers
            related_identifiers = dataset.get('relatedIdentifiers')
            if related_identifiers:
                xml.startElement('relatedIdentifiers', {})
                for related_identifier in related_identifiers:
                    self.render_text_element(xml, 'relatedIdentifier', {
                        'relatedIdentifierType': related_identifier.get('relatedIdentifierType'),
                        'relationType': related_identifier.get('relationType')
                    }, related_identifier.get('relatedIdentifier'))
                xml.endElement('relatedIdentifiers')

            # dataSources
            data_sources = dataset.get('dataSources')
            if data_sources:
                xml.startElement('dataSources', {})
                for data_source in data_sources:
                    self.render_text_element(xml, 'dataSource', {
                        'dataSourceDetail': data_source.get('dataSourceDetail')
                    }, data_source.get('dataSource'))
                xml.endElement('dataSources')

            # software
            software = dataset.get('software')
            if software:
                xml.startElement('software', {})
                for software_type in software:
                    xml.startElement('softwareType', {
                        'type': software_type.get('type')
                    })
                    self.render_text_element(xml, 'softwareName', {
                        'softwareVersion': software_type.get('softwareVersion')
                    }, software_type.get('softwareName'))
                    if 'alternativeSoftwareName' in software_type:
                        self.render_text_element(xml, 'alternativeSoftwareName', {
                            'alternativeSoftwareVersion': software_type.get('alternativeSoftwareVersion')
                        }, software_type.get('alternativeSoftwareName'))

                    xml.endElement('softwareType')
                xml.endElement('software')

            # processing
            processing_list = dataset.get('dataProcessing')
            if processing_list:
                xml.startElement('processing', {})
                for processing in processing_list:
                    self.render_text_element(xml, 'dataProcessing', {}, processing)
                xml.endElement('processing')

            # relatedInformations
            related_informations = dataset.get('relatedInformations')
            if related_informations:
                xml.startElement('relatedInformations', {})
                for related_information in related_informations:
                    self.render_text_element(xml, 'relatedInformation', {
                        'relatedInformationType': related_information.get('relatedInformationType')
                    }, related_information.get('relatedInformation'))
                xml.endElement('relatedInformations')

            # funding_references
            funding_references = dataset.get('fundingReferences')
            if funding_references:
                xml.startElement('fundingReferences', {})
                for funding_reference in funding_references:
                    xml.startElement('fundingReference', {})
                    self.render_text_element(xml, 'funderName', {}, funding_reference.get('funderName'))
                    self.render_text_element(xml, 'funderIdentifier', {
                        'schemeURI': self.scheme_uri.get(funding_reference.get('funderIdentifierType')),
                        'funderIdentifierType': funding_reference.get('funderIdentifierType')
                    }, funding_reference.get('funderIdentifier'))
                    if funding_reference.get('awardNumber'):
                        self.render_text_element(xml, 'awardNumber', {
                            'awardURI': funding_reference.get('awardURI')
                        }, funding_reference.get('awardNumber'))
                    if funding_reference.get('awardTitle'):
                        self.render_text_element(xml, 'awardTitle', {}, funding_reference.get('awardTitle'))
                    xml.endElement('fundingReference')
                xml.endElement('fundingReferences')

            xml.endElement('ns2:radarDataset')

    def render(self, request):
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'filename="%s.zip"' % self.project.title

        zip_file = zipfile.ZipFile(response, 'w')
        for dataset in self.get_datasets():
            xmldata = self.Renderer().render(dataset)
            zip_file.writestr(dataset.get('file_name'), prettify_xml(xmldata))

        return response


class RadarExportProvider(RadarMixin, Export, OauthProviderMixin):

    class Form(forms.Form):

        dataset = forms.CharField(label=_('Select dataset of your project'))
        workspace = forms.CharField(label=_('Select a workspace in RADAR'))

        def __init__(self, *args, **kwargs):
            dataset_choices = kwargs.pop('dataset_choices')
            workspace_choices = kwargs.pop('workspace_choices')
            super().__init__(*args, **kwargs)

            self.fields['dataset'].widget = forms.RadioSelect(choices=dataset_choices)
            self.fields['workspace'].widget = forms.RadioSelect(choices=workspace_choices)

    def render(self, request):
        url = self.get_get_url()
        return self.get(request, url)

    def submit(self, request):
        dataset_choices, workspace_choices = self.get_from_session(request, 'form')
        form = self.Form(
            request.POST,
            dataset_choices=dataset_choices,
            workspace_choices=workspace_choices
        )

        if form.is_valid():
            url = self.get_post_url(form.cleaned_data['workspace'])
            data = self.get_post_data(form.cleaned_data['dataset'])
            return self.post(request, url, data)
        else:
            return render(request, 'plugins/radar.html', {'form': form}, status=200)

    def get_success(self, request, response):
        datasets = self.get_set('project/dataset/id')
        dataset_choices = [(dataset.set_index, dataset.value)for dataset in datasets]
        workspace_choices = [
            (workspace.get('id'), workspace.get('descriptiveMetadata', {}).get('title'))
            for workspace in response.json().get('data', [])
        ]

        self.store_in_session(request, 'form', (dataset_choices, workspace_choices))

        form = self.Form(
            dataset_choices=dataset_choices,
            workspace_choices=workspace_choices
        )

        return render(request, 'plugins/exports_radar.html', {'form': form}, status=200)

    def post_success(self, request, response):
        radar_id = response.json().get('id')
        if radar_id:
            return redirect('{}/radar/de/dataset/{}'.format(self.radar_url, radar_id))
        else:
            return render(request, 'core/error.html', {
                'title': _('RADAR error'),
                'errors': [_('The ID of the new dataset could not be retrieved.')]
            }, status=200)

    @property
    def radar_url(self):
        return settings.RADAR_PROVIDER['radar_url'].strip('/')

    @property
    def authorize_url(self):
        return '{}/radar-backend/oauth/authorize'.format(self.radar_url)

    @property
    def token_url(self):
        return '{}/radar-backend/oauth/token'.format(self.radar_url)

    @property
    def client_id(self):
        return settings.RADAR_PROVIDER['client_id']

    @property
    def client_secret(self):
        return settings.RADAR_PROVIDER['client_secret']

    @property
    def redirect_path(self):
        return reverse('oauth_callback', args=['radar'])

    def get_get_url(self):
        return '{}/radar/api/workspaces'.format(self.radar_url)

    def get_post_url(self, workspace_id):
        return '{}/radar/api/workspaces/{}/datasets'.format(self.radar_url, workspace_id)

    def get_post_data(self, set_index):
        dataset = self.get_dataset(set_index)
        now = int(time.time())

        return {
            'technicalMetadata': {
                "retentionPeriod": 10,
                "archiveDate": now,
                "publishDate": now,
                "responsibleEmail": self.user.email,
                "schema": {
                    "key": "RDDM",
                    "version": "09"
                }
            },
            'descriptiveMetadata': dataset
        }

    def get_authorize_params(self, request, state):
        return {
            'response_type': 'code',
            'client_id': 'jochenklar',
            'redirect_uri': 'https://rdmo.jochenklar.dev/services/oauth/radar/callback/',
            # 'redirect_uri': request.build_absolute_uri(self.redirect_path),
            'state': state
        }

    def get_callback_params(self, request):
        return {
            'grant_type': 'authorization_code',
            # 'redirect_uri': request.build_absolute_uri(self.redirect_path),
            'redirect_uri': 'https://rdmo.jochenklar.dev/services/oauth/radar/callback/',
            'code': request.GET.get('code')
        }

    def get_callback_auth(self, request):
        return (self.client_id, self.client_secret)

    def get_error_message(self, response):
        return response.json().get('exception')
