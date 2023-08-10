class RadarMixin(object):

    identifier_type_options = {
        'identifier_type/doi': 'DOI',
        'identifier_type/url': 'URL',
        'identifier_type/handle': 'HANDLE',
        'identifier_type/other': 'OTHER'
    }

    language_options = {
        'language/en': 'ENG',
        'language/de': 'DEU'
    }

    name_type_options = {
        'name_type/personal': 'Personal',
        'name_type/organizational': 'Organizational'
    }

    name_identifier_scheme_options = {
        'name_identifier_scheme/orcid': 'ORCID',
        'name_identifier_scheme/insi': 'INSI',
        # 'name_identifier_scheme/ror': 'ROR',
        'name_identifier_scheme/grid': 'GRID'
    }

    contributor_type_options = {
        'contributor_type/contact_persion': 'CONTACT_PERSON',
        'contributor_type/data_collector': 'DATA_COLLECTOR',
        'contributor_type/data_curator': 'DATA_CURATOR',
        'contributor_type/data_manager': 'DATA_MANAGER',
        'contributor_type/distributor': 'DISTRIBUTOR',
        'contributor_type/editor': 'EDITOR',
        'contributor_type/hosting_institution': 'HOSTING_INSTITUTION',
        'contributor_type/producer': 'PRODUCER',
        'contributor_type/project_leader': 'PROJECT_LEADER',
        'contributor_type/project_manager': 'PROJECT_MANAGER',
        'contributor_type/project_member': 'PROJECT_MEMBER',
        'contributor_type/registration_agency': 'REGISTRATION_AGENCY',
        'contributor_type/registration_authority': 'REGISTRATION_AUTHORITY',
        'contributor_type/related_person': 'RELATED_PERSON',
        'contributor_type/researcher': 'RESEARCHER',
        'contributor_type/research_group': 'RESEARCH_GROUP',
        # 'contributor_type/rights_holder': 'RightsHolder',
        'contributor_type/sponsor': 'SPONSOR',
        # 'contributor_type/supervisor': 'Supervisor',
        'contributor_type/work_package_leader': 'WORK_PACKAGE_LEADER',
        'contributor_type/other': 'OTHER'
    }

    resource_type_options = {
        'resource_type_general/audiovisual': 'AUDIOVISUAL',
        'resource_type_general/collection': 'COLLECTION',
        'resource_type_general/data_paper': 'DATA_PAPER',
        'resource_type_general/dataset': 'DATASET',
        'resource_type_general/event': 'EVENT',
        'resource_type_general/image': 'IMAGE',
        'resource_type_general/interactive_resource': 'INTERACTIVE_RESOURCE',
        'resource_type_general/model': 'MODEL',
        'resource_type_general/physical_object': 'PHYSICAL_OBJECT',
        'resource_type_general/service': 'SERVICE',
        'resource_type_general/software': 'SOFTWARE',
        'resource_type_general/sound': 'SOUND',
        'resource_type_general/text': 'TEXT',
        'resource_type_general/workflow': 'WORKFLOW',
        'resource_type_general/other': 'OTHER'
    }

    controlled_subject_area_options = {
        'radar_controlled_subject_area/agriculture': 'AGRICULTURE',
        'radar_controlled_subject_area/architecture': 'ARCHITECTURE',
        'radar_controlled_subject_area/arts_and_media': 'ARTS_AND_MEDIA',
        'radar_controlled_subject_area/astrophysics_and_astronomy': 'ASTROPHYSICS_AND_ASTRONOMY',
        'radar_controlled_subject_area/biochemistry': 'BIOCHEMISTRY',
        'radar_controlled_subject_area/biology': 'BIOLOGY',
        'radar_controlled_subject_area/behavioural_sciences': 'BEHAVIOURAL_SCIENCES',
        'radar_controlled_subject_area/chemistry': 'CHEMISTRY',
        'radar_controlled_subject_area/computer_science': 'Computer COMPUTER_SCIENCE',
        'radar_controlled_subject_area/economics': 'ECONOMICS',
        'radar_controlled_subject_area/engineering': 'ENGINEERING',
        'radar_controlled_subject_area/environmental_science_and_ecology': 'ENVIRONMENTAL_SCIENCE_AND_ECOLOGY',
        'radar_controlled_subject_area/ethnology': 'ETHNOLOGY',
        'radar_controlled_subject_area/geological_science': 'GEOLOGICAL_SCIENCE Science',
        'radar_controlled_subject_area/geography': 'GEOGRAPHY',
        'radar_controlled_subject_area/history': 'HISTORY',
        'radar_controlled_subject_area/horticulture': 'HORTICULTURE',
        'radar_controlled_subject_area/information_technology': 'INFORMATION_TECHNOLOGY',
        'radar_controlled_subject_area/life_science': 'LIFE_SCIENCE',
        'radar_controlled_subject_area/linguistics': 'LINGUISTICS',
        'radar_controlled_subject_area/materials_science': 'MATERIALS_SCIENCE',
        'radar_controlled_subject_area/mathematics': 'MATHEMATICS',
        'radar_controlled_subject_area/medicine': 'MEDICINE',
        'radar_controlled_subject_area/philosophy': 'PHILOSOPHY',
        'radar_controlled_subject_area/physics': 'PHYSICS',
        'radar_controlled_subject_area/psychology': 'PSYCHOLOGY',
        'radar_controlled_subject_area/social_sciences': 'SOCIAL_SCIENCES',
        'radar_controlled_subject_area/software_technology': 'SOFTWARE_TECHNOLOGY',
        'radar_controlled_subject_area/sports': 'SPORTS',
        'radar_controlled_subject_area/theology': 'THEOLOGY',
        'radar_controlled_subject_area/veterinary_medicine': 'VETERINARY_MEDICINE',
        'radar_controlled_subject_area/other': 'OTHER'
    }

    data_source_options = {
        'radar_data_source/instrument': 'INSTRUMENT',
        'radar_data_source/media': 'MEDIA',
        'radar_data_source/observation': 'OBSERVATION',
        'radar_data_source/trial': 'TRIAL',
        'radar_data_source/organism': 'ORGANISM',
        'radar_data_source/tissue': 'TISSUE',
        'radar_data_source/other': 'OTHER'
    }

    software_type_options = {
        'radar_software_type/resource_production': 'RESOURCE_PRODUCTION',
        'radar_software_type/resource_processing': 'RESOURCE_PROCESSING',
        'radar_software_type/resource_viewing': 'RESOURCE_VIEWING',
        'radar_software_type/other': 'OTHER'
    }

    controlled_rights_options = {
        'dataset_license_types/71': 'CC_BY_4_0_ATTRIBUTION',
        'dataset_license_types/74': 'CC_BY_ND_4_0_ATTRIBUTION_NO_DERIVS',
        'dataset_license_types/75': 'CC_BY_SA_4_0_ATTRIBUTION_SHARE_ALIKE',
        'dataset_license_types/73': 'CC_BY_NC_4_0_ATTRIBUTION_NON_COMMERCIAL',
        # '': 'CC_BY_NC_SA_4_0_ATTRIBUTION_NON_COMMERCIAL_SHARE_ALIKE',
        # '': 'CC_BY_NC_ND_4_0_ATTRIBUTION_NON_COMMERCIAL_NO_DERIVS',
        'dataset_license_types/cc0': 'CC_0_1_0_UNIVERSAL_PUBLIC_DOMAIN_DEDICATION',
        # '': 'ALL_RIGHTS_RESERVED',
        'dataset_license_types/233': 'OTHER'
    }

    relation_type_options = {
        'relation_type/is_cited_by': 'IS_CITED_BY',
        'relation_type/cites': 'CITES',
        'relation_type/is_supplement_to': 'IS_SUPPLEMENT_TO',
        'relation_type/is_supplemented_by': 'IS_SUPPLEMENTED_BY',
        'relation_type/is_continued_by': 'IS_CONTINUED_BY',
        'relation_type/continues': 'CONTINUES',
        # 'relation_type/describes': 'Describes',
        # 'relation_type/is_described_by': 'IsDescribedBy',
        'relation_type/has_metadata': 'HAS_METADATA',
        'relation_type/is_metadata_for': 'IS_METADATA_FOR',
        # 'relation_type/has_version': 'HasVersion',
        # 'relation_type/is_version_of': 'IsVersionOf',
        'relation_type/is_new_version_of': 'IS_NEW_VERSION_OF',
        'relation_type/is_previous_version_of': 'IS_PREVIOUS_VERSION_OF',
        'relation_type/is_part_of': 'IS_PART_OF',
        'relation_type/has_part': 'HAS_PART',
        # 'relation_type/is_published_in': 'IsPublishedIn',
        'relation_type/is_referenced_by': 'IS_REFERENCED_BY',
        'relation_type/references': 'REFERENCES',
        'relation_type/is_documented_by': 'IS_DOCUMENTED_BY',
        'relation_type/documents': 'DOCUMENTS',
        'relation_type/is_compiled_by': 'IS_COMPILED_BY',
        'relation_type/Compiles': 'COMPILES',
        'relation_type/is_variant_form_of': 'IS_VARIANT_FORM_OF',
        'relation_type/is_original_form_of': 'IS_ORIGINAL_FORM_OF',
        'relation_type/is_identical_to': 'IS_IDENTICAL_TO',
        'relation_type/is_reviewed_by': 'IS_REVIEWED_BY',
        'relation_type/reviews': 'REVIEWS',
        'relation_type/is_derived_from': 'IS_DERIVED_FROM',
        'relation_type/is_source_of': 'IS_SOURCE_OF',
        # 'relation_type/is_required_by': 'IsRequiredBy',
        # 'relation_type/requires': 'Requires',
        # 'relation_type/obsoletes': 'Obsoletes',
        # 'relation_type/is_obsoleted_by': 'IsObsoletedBy'
    }

    def get_dataset(self, set_index):
        dataset = {}

        # # identifier
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
        for creator_set in self.get_set('project/dataset/creator/name', set_prefix=str(set_index)):
            creator = self.get_name('creator', 'project/dataset/creator',
                                    set_prefix=creator_set.set_prefix, set_index=creator_set.set_index)
            if creator:
                if 'creators' not in dataset:
                    dataset['creators'] = {
                        'creator': []
                    }
                dataset['creators']['creator'].append(creator)

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
            dataset['publishers'] = {
                'publisher': [publisher]
            }

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
            dataset['subjectAreas'] = {
                'subjectArea': []
            }
            for subject_area in subject_areas:
                if subject_area.is_true:
                    if subject_area.option:
                        controlled_subject_area_name = self.controlled_subject_area_options.get(subject_area.option.uri_path, 'Other')
                    else:
                        controlled_subject_area_name = 'Other'

                    if controlled_subject_area_name == 'Other':
                        dataset['subjectAreas']['subjectArea'].append({
                            'controlledSubjectAreaName': controlled_subject_area_name,
                            'additionalSubjectAreaName': subject_area.value
                        })
                    else:
                        dataset['subjectAreas']['subjectArea'].append({
                            'controlledSubjectAreaName': controlled_subject_area_name
                        })

        # resource
        resource_type = self.get_text('project/dataset/resource_type', set_index=set_index)
        if resource_type:
            dataset['resource'] = {
                'value': resource_type,
                'resourceType': self.get_option(self.resource_type_options, 'project/dataset/resource_type_general', set_index=set_index)
            }

        dataset['title'] = \
            self.get_text('project/dataset/title', set_index=set_index) or \
            self.get_text('project/dataset/id', set_index=set_index) or \
            'Dataset #{}'.format(set_index + 1)

        # alternate_identifiers
        alternate_identifier_sets = self.get_set('project/dataset/alternate_identifier/identifier', set_prefix=str(set_index))
        if alternate_identifier_sets:
            dataset['alternateIdentifiers'] = {
              'alternateIdentifier': []
            }
            for alternate_identifier_set in alternate_identifier_sets:
                dataset['alternateIdentifiers']['alternateIdentifier'].append({
                    'value': self.get_text('project/dataset/alternate_identifier/identifier',
                                           set_prefix=alternate_identifier_set.set_prefix,
                                           set_index=alternate_identifier_set.set_index),
                    'alternateIdentifierType': self.get_option(self.identifier_type_options,
                                                               'project/dataset/alternate_identifier/identifier_type',
                                                               set_prefix=alternate_identifier_set.set_prefix,
                                                               set_index=alternate_identifier_set.set_index)
                })

        # related_identifiers
        related_identifier_sets = self.get_set('project/dataset/related_identifier/identifier', set_prefix=str(set_index))
        if related_identifier_sets:
            dataset['relatedIdentifiers'] = {
              'relatedIdentifier': []
            }
            for related_identifier_set in related_identifier_sets:
                dataset['relatedIdentifiers']['relatedIdentifier'].append({
                    'value': self.get_text('project/dataset/related_identifier/identifier',
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
                    controlled_rights = self.controlled_rights_options.get(rights.option.uri_path, 'Other')
                else:
                    controlled_rights = 'Other'

                dataset['rights'] = {
                    'controlledRights': controlled_rights,
                    'additionalRights': rights.value if controlled_rights == 'Other' else None
                }

        # rights holders
        rights_holders = self.get_list('project/dataset/sharing/rights_holder', set_index=set_index)
        if rights_holders:
            dataset['rightsHolders'] = {
                'rightsHolder': rights_holders
            }

        # description
        description = self.get_text('project/dataset/description', set_index=set_index)
        if description:
            dataset['descriptions'] = {
                'description': [{
                    'value': description,
                    'descriptionType': 'ABSTRACT'
                }]
            }

        # keywords
        keywords = self.get_list('project/research_question/keywords')
        if keywords:
            dataset['keywords'] = {
                'keyword': keywords
            }

        # contributors
        for contributor_set in self.get_set('project/dataset/contributor/name', set_prefix=str(set_index)):
            contributor = self.get_name('contributor', 'project/dataset/contributor',
                                        set_prefix=contributor_set.set_prefix, set_index=contributor_set.set_index)

            if contributor:
                if 'contributors' not in dataset:
                    dataset['contributors'] = {
                        'contributor': []
                    }
                dataset['contributors']['contributor'].append(contributor)

        # language
        dataset['language'] = self.get_option(self.language_options, 'project/dataset/language', set_index=set_index)

        # dataSource
        data_source = self.get_text('project/dataset/data_source', set_index=set_index)
        if data_source:
            dataset['dataSources'] = {
                'dataSource': [{
                    'value': data_source,
                    'dataSourceDetail': self.get_option(self.data_source_options, 'project/dataset/data_source_detail', set_index=set_index)
                }]
            }

        # dataProcessing
        # data_processing = self.get_list('project/dataset/data_processing', set_index=set_index)
        # if data_processing:
        #     dataset['dataProcessing'] = data_processing

        # funding_references
        funding_reference_sets = self.get_set('project/funder/id')
        if funding_reference_sets:
            dataset['fundingReferences'] = {
                'fundingReference': []
            }
            for funding_reference_set in funding_reference_sets:
                funding_reference = {
                    'funderName': self.get_text('project/funder/name', set_index=funding_reference_set.set_index),
                    'awardURI': self.get_text('project/funder/programme/url', set_index=funding_reference_set.set_index),
                    'awardNumber': self.get_text('project/funder/programme/number', set_index=funding_reference_set.set_index),
                    'awardTitle': self.get_text('project/funder/programme/title', set_index=funding_reference_set.set_index)
                }

                funder_identifier = self.get_text('project/funder/name_identifier', set_index=funding_reference_set.set_index)
                if funder_identifier:
                    funding_reference['funderIdentifier'] = {
                        'value': funder_identifier,
                        'type': self.get_option(self.name_identifier_scheme_options, 'project/funder/name_identifier_scheme',
                                                set_index=funding_reference_set.set_index, default='OTHER')
                    }

                dataset['fundingReferences']['fundingReference'].append(funding_reference)

        return dataset

    def get_name(self, prefix, attribute, set_prefix='', set_index=0):
        name_text = self.get_text(attribute + '/name', set_prefix=set_prefix, set_index=set_index)
        if name_text:
            name = {
                '{}Name'.format(prefix): name_text,
                'nameType': self.get_option(self.name_type_options, attribute + '/name_type',
                                            set_prefix=set_prefix, set_index=set_index, default='Personal'),
            }

            if prefix == 'contributor':
                contributor_type = self.get_option(self.contributor_type_options, attribute + '/contributor_type',
                                                   set_prefix=set_prefix, set_index=set_index, default='OTHER')
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
                name['nameIdentifier'] = [{
                    'value': identifier,
                    'nameIdentifierScheme': self.get_option(self.name_identifier_scheme_options,
                                                            attribute + '/name_identifier_scheme',
                                                            set_prefix=set_prefix, set_index=set_index,
                                                            default='ORCID')
                }]

            # affiliations
            affiliations = self.get_list(attribute + '/affiliation', set_prefix=set_prefix, set_index=set_index)
            if affiliations:
                name['{}Affiliation'.format(prefix)] = affiliations[0]

            return name
        else:
            return None
