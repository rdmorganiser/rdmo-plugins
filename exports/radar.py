import zipfile
from collections import defaultdict

from django.http import HttpResponse
from rdmo.core.exports import prettify_xml
from rdmo.core.renderers import BaseXMLRenderer
from rdmo.projects.exports import Export


class RadarExport(Export):

    scheme_uri = {
        'INSI': 'http://www.isni.org/',
        'ORCID': 'https://orcid.org',
        'ROR': 'https://ror.org/',
        'GRID': 'https://www.grid.ac/'
    }

    identifier_type_options = {
        # '': 'DOI',
        # '': 'Handle'
    }

    language_options = {
        # '': 'eng',
        # '': 'deu'
    }

    name_type_options = {
        # '': 'Personal',
        # '': 'Organizational'
    }

    name_identifier_scheme_options = {
        # '': 'ORCID',
        # '': 'INSI',
        # '': 'ROR',
        # '': 'GRID'
    }

    controlled_subject_area_options = {
        # '': 'Agriculture',
        # '': 'Architecture',
        # '': 'Arts and Media',
        'research_fields/199': 'Astrophysics and Astronomy',
        # '': 'Biochemistry',
        # '': 'Biology',
        # '': 'Behavioural Sciences',
        # '': 'Chemistry',
        'research_fields/215': 'Computer Science',
        # '': 'Economics',
        # '': 'Engineering',
        # '': 'Environmental Science and Ecology',
        # '': 'Ethnology',
        # '': 'Geological Science',
        # '': 'Geography',
        # '': 'History',
        # '': 'Horticulture',
        # '': 'Information Technology',
        # '': 'Life Science',
        # '': 'Linguistics',
        # '': 'Materials Science',
        # '': 'Mathematics',
        # '': 'Medicine',
        # '': 'Philosophy',
        # '': 'Physics',
        # '': 'Psychology',
        # '': 'Social Sciences',
        # '': 'Software Technology',
        # '': 'Sports',
        # '': 'Theology',
        # '': 'Veterinary Medicine',
        # '': 'Other'
    }

    contributor_type_options = {
        # '': 'ContactPerson',
        # '': 'DataCollector',
        # '': 'DataCurator',
        # '': 'DataManager',
        # '': 'Distributor',
        # '': 'Editor',
        # '': 'HostingInstitution',
        # '': 'Producer',
        # '': 'ProjectLeader',
        # '': 'ProjectManager',
        # '': 'ProjectMember',
        # '': '19RegistrationAgency',
        # '': 'RegistrationAuthority',
        # '': 'RelatedPerson',
        # '': 'Researcher',
        # '': 'ResearchGroup',
        # '': 'RightsHolder',
        # '': 'Sponsor',
        # '': 'Supervisor',
        # '': 'WorkPackageLeader',
        # '': 'Other'
    }

    resource_type_options = {
        # '': 'Audiovisual',
        # '': 'Collection',
        # '': 'DataPaper',
        # '': 'Dataset',
        # '': 'Event',
        # '': 'Image',
        # '': 'InteractiveResource',
        # '': 'Model',
        # '': 'PhysicalObject',
        # '': 'Service',
        # '': 'Software',
        # '': 'Sound',
        # '': 'Text',
        # '': 'Workflow',
        # '': 'Other'
    }

    data_source_options = {
        # '': 'Instrument',
        # '': 'Media',
        # '': 'Observation',
        # '': 'Trial',
        # '': 'Organism',
        # '': 'Tissue',
        # '': 'Other'
    }

    software_type_options = {
        # '': 'Resource Production',
        # '': 'Resource Processing',
        # '': 'Resource Viewing'
        # '': 'Other'
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

    class Renderer(BaseXMLRenderer):

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
                        self.render_node('affiliation', {
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
                        self.render_node('affiliation', {
                            'affiliationIdentifier': affiliation.get('affiliationIdentifier'),
                            'affiliationIdentifierScheme': affiliation.get('affiliationIdentifierScheme')
                        }, affiliation.get('affiliation'))

                    xml.endElement('contributor')
                xml.endElement('contributors')

            # language
            language = dataset.get('language')
            if language:
                self.render_text_element(xml, 'language', {}, language)

            # alternateIdentifiers
            alternate_identifiers = dataset.get('alternateIdentifiers')
            if alternate_identifiers:
                xml.startElement('alternateIdentifiers', {})
                for alternate_identifier in alternate_identifiers:
                    self.render_text_element(xml, 'alternateIdentifier', {
                        'alternateIdentifierType': dataset.get('alternateIdentifierType')
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
                    self.render_text_element(xml, 'awardNumber', {
                        'awardURI': funding_reference.get('awardURI')
                    }, funding_reference.get('awardNumber'))
                    self.render_text_element(xml, 'awardTitle', {}, funding_reference.get('awardTitle'))
                    xml.endElement('fundingReference')
                xml.endElement('fundingReferences')

            xml.endElement('ns2:radarDataset')

    def render(self):
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'filename="%s.zip"' % self.project.title

        zip_file = zipfile.ZipFile(response, 'w')
        for dataset in self.get_datasets():
            xmldata = self.Renderer().render(dataset)
            zip_file.writestr(dataset.get('file_name'), prettify_xml(xmldata))

        return response

    def get_datasets(self):
        datasets = []
        for rdmo_dataset in self.get_set('project/dataset/id'):
            index = rdmo_dataset.set_index
            dataset = defaultdict(list)

            # file_name
            dataset['file_name'] = '{}.xml'.format(
                self.get_text('project/dataset/identifier', index) or
                self.get_text('project/dataset/id', index) or
                str(index + 1)
            )

            # identifier
            identifier = self.get_text('project/dataset/identifier', set_index=index)
            if identifier:
                dataset['identifier'] = identifier
                dataset['identifierType'] = \
                    self.get_option(self.identifier_type_options, 'project/dataset/identifier_type', set_index=index) or \
                    self.get_option(self.identifier_type_options, 'project/dataset/pids/system', set_index=index) or \
                    'OTHER'
            else:
                dataset['identifier'] = self.get_text('project/dataset/id')
                dataset['identifierType'] = 'OTHER'

            # creators
            for creator_name in self.get_values('project/dataset/creator/name', index):
                creator = self.get_name('project/dataset/creator', index, creator_name.collection_index)
                if creator:
                    dataset['creators'].append(creator)

            # title
            dataset['title'] =  \
                self.get_text('project/dataset/title', index) or \
                self.get_text('project/dataset/id', index) or \
                'Dataset #{}'.format(index + 1)

            # publisher
            publisher = \
                self.get_text('project/dataset/publisher', index) or \
                self.get_text('project/dataset/preservation/repository')
            if publisher:
                dataset['publisher'] = publisher

            # productionYear
            dataset['productionYear'] = self.get_year('project/dataset/created', index)

            # publicationYear
            dataset['publicationYear'] = \
                self.get_year('project/dataset/issued', index) or \
                self.get_year('project/dataset/data_publication_date', index)

            # subjectArea
            subject_areas = \
                self.get_values('project/dataset/research/subject', index) or \
                self.get_values('project/research_field/title')
            if subject_areas:
                dataset['subjectAreas'] = []
                for subject_area in subject_areas:
                    if subject_area.option:
                        controlled_subject_area_name = self.controlled_subject_area_options.get(subject_area.option.path, 'Other')
                    else:
                        controlled_subject_area_name = 'Other'

                    dataset['subjectAreas'].append({
                        'controlledSubjectAreaName': controlled_subject_area_name,
                        'additionalSubjectAreaName': subject_area.value
                    })

            # resource
            resource_type = self.get_text('project/dataset/resource_type', index)
            if resource_type:
                dataset['resourceType'] = resource_type
                dataset['resourceTypeGeneral'] = \
                    self.get_option(self.resource_type_options, 'project/dataset/resource_type_general', index)

            # rights
            rights_list = self.get_values('project/dataset/sharing/conditions', index)
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

            # description
            description = self.get_text('project/dataset/description', index)
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
            for contributor_name in self.get_values('project/dataset/contributor/name', index):
                contributor = self.get_name('project/dataset/contributor', index, contributor_name.collection_index)
                if contributor:
                    dataset['contributors'].append(contributor)

            # language
            dataset['language'] = self.get_option(self.language_options, 'project/dataset/language', index)

            # dataSource
            data_source = self.get_text('project/dataset/data_source', index)
            if data_source:
                dataset['dataSources'] = [{
                    'dataSource': data_source,
                    'dataSourceType': self.get_option(self.data_source_options, 'project/dataset/data_source_type', index)
                }]

            # dataProcessing
            data_processing = self.get_list('project/dataset/data_processing', index)
            if data_processing:
                dataset['dataProcessing'] = data_processing

            # funding_references
            dataset['fundingReferences'] = []
            for funder in self.get_values('project/funder'):
                dataset['fundingReferences'].append({
                    'funderName': self.get_text('project/funder/name', funder.set_index),
                    'funderIdentifier': self.get_text('project/funder/identifier', funder.set_index),
                    'funderIdentifierType': self.get_text('project/funder/identifier_type', funder.set_index),
                    'awardURI': self.get_text('project/funder/award_uri', funder.set_index),
                    'awardNumber': self.get_text('project/funder/award_number', funder.set_index),
                    'awardTitle': self.get_text('project/funder/award_title', funder.set_index)
                })

            datasets.append(dataset)

        return datasets

    def get_name(self, attribute, set_index=0, collection_index=0):
        name_text = self.get_text(attribute + '/name', set_index=set_index, collection_index=collection_index)
        if name_text:
            name = {
                'name': name_text,
                'nameType': self.get_option(self.name_type_options, attribute + '/name_type',
                                            set_index=set_index, collection_index=collection_index, default='Personal'),
            }

            # contributor_name
            contributor_type = self.get_option(self.contributor_type_options, attribute + '/contributor_type',
                                               set_index=set_index, collection_index=collection_index, default='Other')
            if contributor_type:
                name['contributorType'] = contributor_type

            # given_name
            given_name = self.get_text(attribute + '/given_name',
                                       set_index=set_index, collection_index=collection_index)
            if given_name:
                name['givenName'] = given_name

            # family_name
            family_name = self.get_text(attribute + '/family_name',
                                        set_index=set_index, collection_index=collection_index)
            if family_name:
                name['familyName'] = family_name

            # identifier
            identifier = self.get_text(attribute + '/identifier',
                                       set_index=set_index, collection_index=collection_index)
            if identifier:
                name['nameIdentifier'] = identifier
                name['nameIdentifierScheme'] = self.get_option(self.name_identifier_scheme_options,
                                                               attribute + '/identifier_type',
                                                               set_index=set_index, collection_index=collection_index,
                                                               default='ORCID')
            return name
        else:
            return None
