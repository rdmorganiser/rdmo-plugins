from collections import defaultdict

from django.http import HttpResponse

from rdmo.core.exports import prettify_xml
from rdmo.core.renderers import BaseXMLRenderer
from rdmo.projects.exports import Export


class DataCiteExport(Export):

    scheme_uri = {
        'INSI': 'http://www.isni.org/',
        'ORCID': 'https://orcid.org',
        'ROR': 'https://ror.org/',
        'GRID': 'https://www.grid.ac/'
    }

    identifier_type_options = {
        # '': 'DOI',
        # '': 'OTHER'
    }

    language_options = {
        # '': 'en-US',
        # '': 'de-de'
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

    resource_type_general_options = {
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

    rights_uri_options = {
        'dataset_license_types/71': 'https://creativecommons.org/licenses/by/4.0/',
        'dataset_license_types/73': 'https://creativecommons.org/licenses/by-nc/4.0/',
        'dataset_license_types/74': 'https://creativecommons.org/licenses/by-nd/4.0/',
        'dataset_license_types/75': 'https://creativecommons.org/licenses/by-sa/4.0/',
        'dataset_license_types/cc0': 'https://creativecommons.org/publicdomain/zero/1.0/deed.de'
    }

    class DataCiteRenderer(BaseXMLRenderer):

        def render_document(self, xml, datasets):
            self.render_resources(xml, datasets)

        def render_resources(self, xml, datasets):
            xml.startElement('resources', {})
            for dataset in datasets:
                self.render_resource(xml, dataset)
            xml.endElement('resources')

        def render_resource(self, xml, dataset):
            xml.startElement('resource', {
                'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                'xmlns': 'http://datacite.org/schema/kernel-4',
                'xsi:schemaLocation': 'http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.3/metadata.xsd'
            })

            # identifier
            self.render_text_element(xml, 'identifier', {
                'identifierType': dataset.get('identifierType', 'OTHER')
            }, dataset.get('identifier'))

            # creators
            xml.startElement('creators', {})
            for creator in dataset.get('creators', []):
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

            # titles
            xml.startElement('titles', {})
            self.render_text_element(xml, 'title', {}, dataset.get('title'))
            xml.endElement('titles')

            # publisher
            self.render_text_element(xml, 'publisher', {}, dataset.get('publisher'))

            # publicationYear
            self.render_text_element(xml, 'publicationYear', {}, dataset.get('publicationYear'))

            # subjects
            xml.startElement('subjects', {})
            for subject in dataset.get('subjects', []):
                self.render_text_element(xml, 'subject', {}, subject)
            xml.endElement('subjects')

            # contributors
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

            # dates
            xml.startElement('dates', {})
            if dataset.get('created'):
                self.render_text_element(xml, 'date', {
                    'dateType': 'Created'
                }, dataset.get('created'))
            if dataset.get('issued'):
                self.render_text_element(xml, 'date', {
                    'dateType': 'Issued'
                }, dataset.get('issued'))
            xml.endElement('dates')

            # language
            self.render_text_element(xml, 'language', {}, dataset.get('language'))

            # resource_type
            if dataset.get('resourceType'):
                self.render_text_element(xml, 'resourceType', {
                    'resourceTypeGeneral': dataset.get('resourceTypeGeneral')
                }, dataset.get('resourceType'))

            # alternate_identifiers
            xml.startElement('alternateIdentifiers', {})
            for alternate_identifier in dataset.get('alternateIdentifiers', []):
                self.render_text_element(xml, 'alternateIdentifier', {
                    'alternateIdentifierType': dataset.get('alternateIdentifierType')
                }, alternate_identifier.get('alternateIdentifier'))
            xml.endElement('alternateIdentifiers')

            # related_identifiers
            xml.startElement('relatedIdentifiers', {})
            for related_identifier in dataset.get('relatedIdentifiers', []):
                self.render_text_element(xml, 'relatedIdentifier', {
                    'relatedIdentifierType': related_identifier.get('relatedIdentifierType'),
                    'relationType': related_identifier.get('relationType')
                }, related_identifier.get('relatedIdentifier'))
            xml.endElement('relatedIdentifiers')

            # rights list
            xml.startElement('rightsList', {})
            for rights in dataset.get('rightsList', []):
                self.render_text_element(xml, 'rights', {
                    'rightsURI': rights.get('rightsURI')
                }, rights.get('rights'))
            xml.endElement('rightsList')

            # descriptions
            xml.startElement('descriptions', {})
            if dataset.get('description'):
                self.render_text_element(xml, 'description', {
                    'descriptionType': 'Abstract'
                }, dataset.get('description'))
            xml.endElement('descriptions')

            # funding_references
            xml.startElement('fundingReferences', {})
            for funding_reference in dataset.get('fundingReferences', []):
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

            xml.endElement('resource')

    def render(self):
        datasets = self.get_datasets()
        xmldata = self.DataCiteRenderer().render(datasets)
        response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
        response['Content-Disposition'] = 'filename="%s.xml"' % self.project.title
        return response

    def get_datasets(self):
        datasets = []
        for rdmo_dataset in self.get_set('project/dataset/id'):
            index = rdmo_dataset.set_index
            dataset = defaultdict(list)

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

            # titles
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

            # publication_year
            dataset['publicationYear'] = self.get_year('project/dataset/data_publication_date', index)

            # subjects
            subjects = \
                self.get_values('project/dataset/research/subject', index) or \
                self.get_values('project/research_field/title')
            if subjects:
                dataset['subjects'] = [subject.value for subject in subjects]

            # contributors
            for contributor_name in self.get_values('project/dataset/contributor/name', index):
                contributor = self.get_name('project/dataset/contributor', index, contributor_name.collection_index)
                if contributor:
                    dataset['contributors'].append(contributor)

            # dates
            dataset['created'] =  \
                self.get_timestamp('project/dataset/date/created', index)
            dataset['issued'] =  \
                self.get_timestamp('project/dataset/date/issued', index) or \
                self.get_timestamp('project/dataset/data_publication_date', index)

            # language
            dataset['language'] = self.get_option(self.language_options, 'project/dataset/language', index)

            # resource_type
            resource_type = self.get_text('project/dataset/resource_type', index)
            if resource_type:
                dataset['resourceType'] = resource_type
                dataset['resourceTypeGeneral'] = \
                    self.get_option(self.resource_type_general_options, 'project/dataset/resource_type_general', index)

            # rights
            for value in self.get_values('project/dataset/sharing/conditions', index):
                dataset['rights_list'].append({
                    'rights': value.value,
                    'rightsURI': self.rights_uri_options[value.option.path]
                })

            # description
            dataset['description'] = self.get_text('project/dataset/description', index)

            # funding_references
            for funder in self.get_values('project/funder'):
                dataset['funding_reference'].append({
                    'funderName': self.get_text('project/funder/name', funder.index),
                    'funderIdentifier': self.get_text('project/funder/identifier', funder.index),
                    'funderIdentifierType': self.get_text('project/funder/identifier_type', funder.index),
                    'awardURI': self.get_text('project/funder/award_uri', funder.index),
                    'awardNumber': self.get_text('project/funder/award_number', funder.index),
                    'awardTitle': self.get_text('project/funder/award_title', funder.index)
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
