import zipfile
from collections import defaultdict

from django.http import HttpResponse
from rdmo.core.exports import prettify_xml
from rdmo.projects.exports import Export
from rocrate.rocrate import ROCrate


class ROCrateExport(Export):
    # identifier_type_options = {
    #     'identifier_type/doi': 'DOI',
    #     'identifier_type/other': 'OTHER'
    # }

    # language_options = {
    #     'language/en': 'en-US',
    #     'language/de': 'de-de'
    # }

    # name_type_options = {
    #     'name_type/personal': 'Personal',
    #     'name_type/organizational': 'Organizational'
    # }

    # name_identifier_scheme_options = {
    #     'name_identifier_scheme/orcid': 'ORCID',
    #     'name_identifier_scheme/insi': 'INSI',
    #     'name_identifier_scheme/ror': 'ROR',
    #     'name_identifier_scheme/grid': 'GRID'
    # }

    # contributor_type_options = {
    #     'contributor_type/contact_persion': 'ContactPerson',
    #     'contributor_type/data_collector': 'DataCollector',
    #     'contributor_type/data_curator': 'DataCurator',
    #     'contributor_type/data_manager': 'DataManager',
    #     'contributor_type/distributor': 'Distributor',
    #     'contributor_type/editor': 'Editor',
    #     'contributor_type/hosting_institution': 'HostingInstitution',
    #     'contributor_type/producer': 'Producer',
    #     'contributor_type/project_leader': 'ProjectLeader',
    #     'contributor_type/project_manager': 'ProjectManager',
    #     'contributor_type/project_member': 'ProjectMember',
    #     'contributor_type/registration_agency': 'RegistrationAgency',
    #     'contributor_type/registration_authority': 'RegistrationAuthority',
    #     'contributor_type/related_person': 'RelatedPerson',
    #     'contributor_type/researcher': 'Researcher',
    #     'contributor_type/research_group': 'ResearchGroup',
    #     'contributor_type/rights_holder': 'RightsHolder',
    #     'contributor_type/sponsor': 'Sponsor',
    #     'contributor_type/supervisor': 'Supervisor',
    #     'contributor_type/work_package_leader': 'WorkPackageLeader',
    #     'contributor_type/other': 'Other'
    # }

    # resource_type_general_options = {
    #     'resource_type_general/audiovisual': 'Audiovisual',
    #     'resource_type_general/collection': 'Collection',
    #     'resource_type_general/data_paper': 'DataPaper',
    #     'resource_type_general/dataset': 'Dataset',
    #     'resource_type_general/event': 'Event',
    #     'resource_type_general/image': 'Image',
    #     'resource_type_general/interactive_resource': 'InteractiveResource',
    #     'resource_type_general/model': 'Model',
    #     'resource_type_general/physical_object': 'PhysicalObject',
    #     'resource_type_general/service': 'Service',
    #     'resource_type_general/software': 'Software',
    #     'resource_type_general/sound': 'Sound',
    #     'resource_type_general/text': 'Text',
    #     'resource_type_general/workflow': 'Workflow',
    #     'resource_type_general/other': 'Other'
    # }

    # rights_uri_options = {
    #     'dataset_license_types/71': 'https://creativecommons.org/licenses/by/4.0/',
    #     'dataset_license_types/73': 'https://creativecommons.org/licenses/by-nc/4.0/',
    #     'dataset_license_types/74': 'https://creativecommons.org/licenses/by-nd/4.0/',
    #     'dataset_license_types/75': 'https://creativecommons.org/licenses/by-sa/4.0/',
    #     'dataset_license_types/cc0': 'https://creativecommons.org/publicdomain/zero/1.0/deed.de'
    # }

    # relation_type_options = {
    #     'relation_type/is_cited_by': 'IsCitedBy',
    #     'relation_type/cites': 'Cites',
    #     'relation_type/is_supplement_to': 'IsSupplementTo',
    #     'relation_type/is_supplemented_by': 'IsSupplementedBy',
    #     'relation_type/is_continued_by': 'IsContinuedBy',
    #     'relation_type/continues': 'Continues',
    #     'relation_type/describes': 'Describes',
    #     'relation_type/is_described_by': 'IsDescribedBy',
    #     'relation_type/has_metadata': 'HasMetadata',
    #     'relation_type/is_metadata_for': 'IsMetadataFor',
    #     'relation_type/has_version': 'HasVersion',
    #     'relation_type/is_version_of': 'IsVersionOf',
    #     'relation_type/is_new_version_of': 'IsNewVersionOf',
    #     'relation_type/is_previous_version_of': 'IsPreviousVersionOf',
    #     'relation_type/is_part_of': 'IsPartOf',
    #     'relation_type/has_part': 'HasPart',
    #     'relation_type/is_published_in': 'IsPublishedIn',
    #     'relation_type/is_referenced_by': 'IsReferencedBy',
    #     'relation_type/references': 'References',
    #     'relation_type/is_documented_by': 'IsDocumentedBy',
    #     'relation_type/documents': 'Documents',
    #     'relation_type/is_compiled_by': 'IsCompiledBy',
    #     'relation_type/Compiles': 'Compiles',
    #     'relation_type/is_variant_form_of': 'IsVariantFormOf',
    #     'relation_type/is_original_form_of': 'IsOriginalFormOf',
    #     'relation_type/is_identical_to': 'IsIdenticalTo',
    #     'relation_type/is_reviewed_by': 'IsReviewedBy',
    #     'relation_type/reviews': 'Reviews',
    #     'relation_type/is_derived_from': 'IsDerivedFrom',
    #     'relation_type/is_source_of': 'IsSourceOf',
    #     'relation_type/is_required_by': 'IsRequiredBy',
    #     'relation_type/requires': 'Requires',
    #     'relation_type/obsoletes': 'Obsoletes',
    #     'relation_type/is_obsoleted_by': 'IsObsoletedBy'
    # }

    def render(self):
        response = HttpResponse(
            json.dumps({"dmp": self.get_rocrate()}, indent=2),
            content_type="application/json",
        )
        response["Content-Disposition"] = 'filename="%s.json"' % self.project.title
        return response

    def get_rocrate(self):
        crate = ROCrate()
        crate.name = self.project.title
        crate.description = self.project.description
        crate.keywords = self.get_list("project/research_question/keywords")

        for dataset in self.get_datasets():
            dataset_properties = {"name": dataset["title"]}
            if dataset.get("description"):
                dataset_properties["description"] = dataset["descriptions"]

            crate.add_directory(dataset["filename"], properties=dataset_properties)

        # scheme_uri = {
        #     'INSI': 'http://www.isni.org/',
        #     'ORCID': 'https://orcid.org',
        #     'ROR': 'https://ror.org/',
        #     'GRID': 'https://www.grid.ac/'
        # }

        # def render_document(self, xml, dataset):
        #     xml.startElement('resource', {
        #         'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        #         'xmlns': 'http://datacite.org/schema/kernel-4',
        #         'xsi:schemaLocation': 'http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.3/metadata.xsd'
        #     })

        #     # identifier
        #     identifier = dataset.get('identifier')
        #     if identifier:
        #         self.render_text_element(xml, 'identifier', {
        #             'identifierType': dataset.get('identifierType', 'OTHER')
        #         }, identifier)

        #     # creators
        #     creators = dataset.get('creators')
        #     if creators:
        #         xml.startElement('creators', {})
        #         for creator in creators:
        #             xml.startElement('creator', {})
        #             self.render_text_element(xml, 'creatorName', {
        #                 'nameType': creator.get('nameType')
        #             }, creator.get('name'))

        #             if creator.get('givenName'):
        #                 self.render_text_element(xml, 'givenName', {}, creator.get('givenName'))

        #             if creator.get('familyName'):
        #                 self.render_text_element(xml, 'familyName', {}, creator.get('familyName'))

        #             if creator.get('nameIdentifier'):
        #                 self.render_text_element(xml, 'nameIdentifier', {
        #                     'nameIdentifierScheme': creator.get('nameIdentifierScheme'),
        #                     'schemeURI': self.scheme_uri.get(creator.get('schemeURI')),
        #                 }, creator.get('nameIdentifier'))

        #             for affiliation in creator.get('affiliations', []):
        #                 self.render_text_element(xml, 'affiliation', {
        #                     'affiliationIdentifier': affiliation.get('affiliationIdentifier'),
        #                     'affiliationIdentifierScheme': affiliation.get('affiliationIdentifierScheme')
        #                 }, affiliation.get('affiliation'))

        #             xml.endElement('creator')
        #         xml.endElement('creators')

        #     # titles
        #     titles = dataset.get('titles')
        #     if titles:
        #         xml.startElement('titles', {})
        #         for title in titles:
        #             self.render_text_element(xml, 'title', {
        #                 'titleType': title.get('titleType')
        #             }, title.get('title'))
        #         xml.endElement('titles')

        #     # publisher
        #     publisher = dataset.get('publisher')
        #     if publisher:
        #         self.render_text_element(xml, 'publisher', {}, publisher)

        #     # publicationYear
        #     publication_year = dataset.get('publicationYear')
        #     if publication_year:
        #         self.render_text_element(xml, 'publicationYear', {}, publication_year)

        #     # subjects
        #     subjects = dataset.get('subjects')
        #     if subjects:
        #         xml.startElement('subjects', {})
        #         for subject in subjects:
        #             self.render_text_element(xml, 'subject', {
        #                 'subjectScheme': subject.get('subjectScheme'),
        #                 'schemeURI': subject.get('schemeURI')
        #             }, subject.get('subject'))
        #         xml.endElement('subjects')

        #     # contributors
        #     contributors = dataset.get('contributors')
        #     if contributors:
        #         xml.startElement('contributors', {})
        #         for contributor in dataset.get('contributors', []):
        #             xml.startElement('contributor', {
        #                 'contributorType': contributor.get('contributorType')
        #             })
        #             self.render_text_element(xml, 'contributorName', {
        #                 'nameType': contributor.get('nameType')
        #             }, contributor.get('name'))

        #             if contributor.get('givenName'):
        #                 self.render_text_element(xml, 'givenName', {}, contributor.get('givenName'))

        #             if contributor.get('familyName'):
        #                 self.render_text_element(xml, 'familyName', {}, contributor.get('familyName'))

        #             if contributor.get('nameIdentifier'):
        #                 self.render_text_element(xml, 'nameIdentifier', {
        #                     'nameIdentifierScheme': contributor.get('nameIdentifierScheme'),
        #                     'schemeURI': self.scheme_uri.get(contributor.get('schemeURI')),
        #                 }, contributor.get('nameIdentifier'))

        #             for affiliation in contributor.get('affiliations', []):
        #                 self.render_text_element(xml, 'affiliation', {
        #                     'affiliationIdentifier': affiliation.get('affiliationIdentifier'),
        #                     'affiliationIdentifierScheme': affiliation.get('affiliationIdentifierScheme')
        #                 }, affiliation.get('affiliation'))

        #             xml.endElement('contributor')
        #         xml.endElement('contributors')

        #     # dates
        #     created = dataset.get('created')
        #     issued = dataset.get('issued')
        #     if created or issued:
        #         xml.startElement('dates', {})
        #         if created:
        #             self.render_text_element(xml, 'date', {
        #                 'dateType': 'Created'
        #             }, created)
        #         if issued:
        #             self.render_text_element(xml, 'date', {
        #                 'dateType': 'Issued'
        #             }, issued)
        #         xml.endElement('dates')

        #     # language
        #     language = dataset.get('language')
        #     if language:
        #         self.render_text_element(xml, 'language', {}, language)

        #     # resource_type
        #     resource_type = dataset.get('resourceType')
        #     if resource_type:
        #         self.render_text_element(xml, 'resourceType', {
        #             'resourceTypeGeneral': dataset.get('resourceTypeGeneral')
        #         }, resource_type)

        #     # alternateIdentifiers
        #     alternate_identifiers = dataset.get('alternateIdentifiers')
        #     if alternate_identifiers:
        #         xml.startElement('alternateIdentifiers', {})
        #         for alternate_identifier in alternate_identifiers:
        #             self.render_text_element(xml, 'alternateIdentifier', {
        #                 'alternateIdentifierType': alternate_identifier.get('alternateIdentifierType')
        #             }, alternate_identifier.get('alternateIdentifier'))
        #         xml.endElement('alternateIdentifiers')

        #     # related_identifiers
        #     related_identifiers = dataset.get('relatedIdentifiers')
        #     if related_identifiers:
        #         xml.startElement('relatedIdentifiers', {})
        #         for related_identifier in related_identifiers:
        #             self.render_text_element(xml, 'relatedIdentifier', {
        #                 'relatedIdentifierType': related_identifier.get('relatedIdentifierType'),
        #                 'relationType': related_identifier.get('relationType')
        #             }, related_identifier.get('relatedIdentifier'))
        #         xml.endElement('relatedIdentifiers')

        #     # rights list
        #     rights_list = dataset.get('rightsList')
        #     if rights_list:
        #         xml.startElement('rightsList', {})
        #         for rights in rights_list:
        #             self.render_text_element(xml, 'rights', {
        #                 'rightsURI': rights.get('rightsURI')
        #             }, rights.get('rights'))
        #         xml.endElement('rightsList')

        #     # descriptions
        #     descriptions = dataset.get('descriptions')
        #     if descriptions:
        #         xml.startElement('descriptions', {})
        #         for description in descriptions:
        #             self.render_text_element(xml, 'description', {
        #                 'descriptionType': description.get('descriptionType', 'Abstract')
        #             }, description.get('description'))
        #         xml.endElement('descriptions')

        #     # funding_references
        #     funding_references = dataset.get('fundingReferences')
        #     if funding_references:
        #         xml.startElement('fundingReferences', {})
        #         for funding_reference in funding_references:
        #             xml.startElement('fundingReference', {})
        #             self.render_text_element(xml, 'funderName', {}, funding_reference.get('funderName'))
        #             self.render_text_element(xml, 'funderIdentifier', {
        #                 'schemeURI': self.scheme_uri.get(funding_reference.get('funderIdentifierType')),
        #                 'funderIdentifierType': funding_reference.get('funderIdentifierType')
        #             }, funding_reference.get('funderIdentifier'))
        #             if funding_reference.get('awardNumber'):
        #                 self.render_text_element(xml, 'awardNumber', {
        #                     'awardURI': funding_reference.get('awardURI')
        #                 }, funding_reference.get('awardNumber'))
        #             if funding_reference.get('awardTitle'):
        #                 self.render_text_element(xml, 'awardTitle', {}, funding_reference.get('awardTitle'))
        #             xml.endElement('fundingReference')
        #         xml.endElement('fundingReferences')

        #     xml.endElement('resource')

    def render(self):
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = 'filename="%s.zip"' % self.project.title

        zip_file = zipfile.ZipFile(response, "w")
        for dataset in self.get_datasets():
            xmldata = self.Renderer().render(dataset)
            zip_file.writestr(dataset.get("file_name"), prettify_xml(xmldata))

        return response

    def get_datasets(self):
        datasets = []
        for rdmo_dataset in self.get_set("project/dataset/id"):
            set_index = rdmo_dataset.set_index
            dataset = defaultdict(list)

            # file_name
            dataset["file_name"] = "./{}".format(
                self.get_text("project/dataset/identifier", set_index=set_index)
                or self.get_text("project/dataset/id", set_index=set_index)
                or str(set_index + 1)
            )

            # identifier
            # identifier = self.get_text('project/dataset/identifier', set_index=set_index)
            # if identifier:
            #     dataset['identifier'] = identifier
            #     dataset['identifierType'] = \
            #         self.get_option(self.identifier_type_options, 'project/dataset/identifier_type', set_index=set_index) or \
            #         self.get_option(self.identifier_type_options, 'project/dataset/pids/system', set_index=set_index) or \
            #         'OTHER'
            # else:
            #     dataset['identifier'] = self.get_text('project/dataset/id', set_index=set_index)
            #     dataset['identifierType'] = 'OTHER'

            # creators
            # for creator_set in self.get_set('project/dataset/creator/name', set_prefix=str(set_index)):
            #     creator = self.get_name('project/dataset/creator',
            #                             set_prefix=creator_set.set_prefix, set_index=creator_set.set_index)
            #     if creator:
            #         dataset['creators'].append(creator)

            # titles
            dataset["title"] = (
                self.get_text("project/dataset/title", set_index=set_index)
                or self.get_text("project/dataset/id", set_index=set_index)
                or "Dataset #{}".format(set_index + 1)
            )

            # publisher
            # publisher = \
            #     self.get_text('project/dataset/publisher', set_index=set_index) or \
            #     self.get_text('project/dataset/preservation/repository', set_index=set_index)
            # if publisher:
            #     dataset['publisher'] = publisher

            # publication_year
            # dataset['publicationYear'] = self.get_year('project/dataset/data_publication_date', set_index=set_index)

            # subjects
            # subjects = \
            #     self.get_values('project/dataset/subject', set_index=set_index) or \
            #     self.get_values('project/research_field/title', set_index=set_index)
            # if subjects:
            #     dataset['subjects'] = [{
            #         'subject': subject.value
            #     } for subject in subjects]

            # contributors
            # for contributor_set in self.get_set('project/dataset/contributor/name', set_prefix=str(set_index)):
            #     contributor = self.get_name('project/dataset/contributor',
            #                                 set_prefix=contributor_set.set_prefix, set_index=contributor_set.set_index)
            #     if contributor:
            #         dataset['contributors'].append(contributor)

            # dates
            # dataset['created'] =  \
            #     self.get_timestamp('project/dataset/date/created', set_index=set_index)
            # dataset['issued'] =  \
            #     self.get_timestamp('project/dataset/date/issued', set_index=set_index) or \
            #     self.get_timestamp('project/dataset/data_publication_date', set_index=set_index)

            # language
            # dataset['language'] = self.get_option(self.language_options, 'project/dataset/language', set_index=set_index)

            # resource_type
            # resource_type = self.get_text('project/dataset/resource_type', set_index=set_index)
            # if resource_type:
            #     dataset['resourceType'] = resource_type
            #     dataset['resourceTypeGeneral'] = \
            #         self.get_option(self.resource_type_general_options, 'project/dataset/resource_type_general', set_index=set_index)

            # alternate_identifiers
            # for alternate_identifier_set in self.get_set('project/dataset/alternate_identifier/identifier', set_prefix=str(set_index)):
            #     dataset['alternateIdentifiers'].append({
            #         'alternateIdentifier': self.get_text('project/dataset/alternate_identifier/identifier',
            #                                              set_prefix=alternate_identifier_set.set_prefix,
            #                                              set_index=alternate_identifier_set.set_index),
            #         'alternateIdentifierType': self.get_option(self.identifier_type_options,
            #                                                    'project/dataset/alternate_identifier/identifier_type',
            #                                                    set_prefix=alternate_identifier_set.set_prefix,
            #                                                    set_index=alternate_identifier_set.set_index)
            #     })

            # related_identifiers
            # for related_identifier_set in self.get_set('project/dataset/related_identifier/identifier', set_prefix=str(set_index)):
            #     dataset['relatedIdentifiers'].append({
            #         'relatedIdentifier': self.get_text('project/dataset/related_identifier/identifier',
            #                                            set_prefix=related_identifier_set.set_prefix,
            #                                            set_index=related_identifier_set.set_index),
            #         'relatedIdentifierType': self.get_option(self.identifier_type_options,
            #                                                  'project/dataset/related_identifier/identifier_type',
            #                                                  set_prefix=related_identifier_set.set_prefix,
            #                                                  set_index=related_identifier_set.set_index),
            #         'relationType': self.get_option(self.relation_type_options,
            #                                         'project/dataset/related_identifier/relation_type',
            #                                         set_prefix=related_identifier_set.set_prefix,
            #                                         set_index=related_identifier_set.set_index)
            #     })

            # rights
            # for rights in self.get_values('project/dataset/sharing/conditions', set_index=set_index):
            #     if rights.option:
            #         dataset['rightsList'].append({
            #             'rights': rights.value,
            #             'rightsURI': self.rights_uri_options.get(rights.option.path)
            #         })

            # description
            description = self.get_text(
                "project/dataset/description", set_index=set_index
            )
            if description:
                dataset["description"] = description

            # funding_references
            # for funder in self.get_set('project/funder/id'):
            #     dataset['fundingReferences'].append({
            #         'funderName': self.get_text('project/funder/name', set_index=funder.set_index),
            #         'funderIdentifier': self.get_text('project/funder/name_identifier', set_index=funder.set_index),
            #         'funderIdentifierType': self.get_option(self.name_identifier_scheme_options, 'project/funder/name_identifier_scheme', set_index=funder.set_index),
            #         'awardURI': self.get_text('project/funder/programme/url', set_index=funder.set_index),
            #         'awardNumber': self.get_text('project/funder/programme/number', set_index=funder.set_index),
            #         'awardTitle': self.get_text('project/funder/programme/title', set_index=funder.set_index)
            #     })

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
