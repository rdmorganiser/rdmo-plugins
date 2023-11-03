import mimetypes

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rdmo.core.constants import VALUE_TYPE_DATETIME
from rdmo.core.xml import get_ns_map, read_xml_file
from rdmo.projects.imports import Import
from rdmo.projects.models import Value


class RadarImport(Import):

    identifier_type_options = {
        'https://rdmo.jochenklar.dev/terms/options/identifier_type/doi': 'DOI',
        'https://rdmo.jochenklar.dev/terms/options/identifier_type/url': 'URL',
        'https://rdmo.jochenklar.dev/terms/options/identifier_type/other': 'OTHER'
    }

    language_options = {
        'https://rdmo.jochenklar.dev/terms/options/language/en': 'eng',
        'https://rdmo.jochenklar.dev/terms/options/language/de': 'deu'
    }

    name_type_options = {
        'https://rdmo.jochenklar.dev/terms/options/name_type/personal': 'Personal',
        'https://rdmo.jochenklar.dev/terms/options/name_type/organizational': 'Organizational'
    }

    name_identifier_scheme_options = {
        'https://rdmo.jochenklar.dev/terms/options/name_identifier_scheme/orcid': 'ORCID',
        'https://rdmo.jochenklar.dev/terms/options/name_identifier_scheme/insi': 'INSI',
        'https://rdmo.jochenklar.dev/terms/options/name_identifier_scheme/ror': 'ROR',
        'https://rdmo.jochenklar.dev/terms/options/name_identifier_scheme/grid': 'GRID'
    }

    contributor_type_options = {
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/contact_persion': 'ContactPerson',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/data_collector': 'DataCollector',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/data_curator': 'DataCurator',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/data_manager': 'DataManager',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/distributor': 'Distributor',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/editor': 'Editor',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/hosting_institution': 'HostingInstitution',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/producer': 'Producer',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/project_leader': 'ProjectLeader',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/project_manager': 'ProjectManager',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/project_member': 'ProjectMember',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/registration_agency': 'RegistrationAgency',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/registration_authority': 'RegistrationAuthority',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/related_person': 'RelatedPerson',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/researcher': 'Researcher',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/research_group': 'ResearchGroup',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/rights_holder': 'RightsHolder',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/sponsor': 'Sponsor',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/supervisor': 'Supervisor',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/work_package_leader': 'WorkPackageLeader',
        'https://rdmo.jochenklar.dev/terms/options/contributor_type/other': 'Other'
    }

    resource_type_general_options = {
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/audiovisual': 'Audiovisual',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/collection': 'Collection',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/data_paper': 'DataPaper',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/dataset': 'Dataset',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/event': 'Event',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/image': 'Image',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/interactive_resource': 'InteractiveResource',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/model': 'Model',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/physical_object': 'PhysicalObject',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/service': 'Service',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/software': 'Software',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/sound': 'Sound',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/text': 'Text',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/workflow': 'Workflow',
        'https://rdmo.jochenklar.dev/terms/options/resource_type_general/other': 'Other'
    }

    controlled_subject_area_options = {
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/agriculture': 'Agriculture',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/architecture': 'Architecture',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/arts_and_media': 'Arts and Media',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/astrophysics_and_astronomy': 'Astrophysics and Astronomy',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/biochemistry': 'Biochemistry',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/biology': 'Biology',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/behavioural_sciences': 'Behavioural Sciences',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/chemistry': 'Chemistry',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/computer_science': 'Computer Science',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/economics': 'Economics',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/engineering': 'Engineering',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/environmental_science_and_ecology': 'Environmental Science and Ecology',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/ethnology': 'Ethnology',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/geological_science': 'Geological Science',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/geography': 'Geography',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/history': 'History',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/horticulture': 'Horticulture',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/information_technology': 'Information Technology',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/life_science': 'Life Science',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/linguistics': 'Linguistics',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/materials_science': 'Materials Science',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/mathematics': 'Mathematics',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/medicine': 'Medicine',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/philosophy': 'Philosophy',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/physics': 'Physics',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/psychology': 'Psychology',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/social_sciences': 'Social Sciences',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/software_technology': 'Software Technology',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/sports': 'Sports',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/theology': 'Theology',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/veterinary_medicine': 'Veterinary Medicine',
        'https://rdmo.jochenklar.dev/terms/options/radar_controlled_subject_area/other': 'Other'
    }

    controlled_rights_options = {
        'https://rdmorganiser.github.io/terms/options/dataset_license_types/71': 'CC BY 4.0 Attribution',
        'https://rdmorganiser.github.io/terms/options/dataset_license_types/74': 'CC BY-ND 4.0 Attribution-NoDerivs',
        'https://rdmorganiser.github.io/terms/options/dataset_license_types/75': 'CC BY-SA 4.0 Attribution-ShareAlike',
        'https://rdmorganiser.github.io/terms/options/dataset_license_types/73': 'CC BY-NC 4.0 Attribution-NonCommercial',
        # '': 'CC BY-NC-SA 4.0 Attribution-NonCommercial-ShareAlike',
        # '': 'CC BY-NC-ND 4.0 Attribution-NonCommercial-NoDerivs',
        'https://rdmorganiser.github.io/terms/options/dataset_license_types/cc0': 'CC0 1.0 Universal Public Domain Dedication',
        # '': 'All rights reserved',
        'https://rdmorganiser.github.io/terms/options/dataset_license_types/233': 'Other'
    }

    data_source_options = {
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/instrument': 'Instrument',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/media': 'Media',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/observation': 'Observation',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/trial': 'Trial',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/organism': 'Organism',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/tissue': 'Tissue',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/other': 'Other'
    }

    relation_type_options = {
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_cited_by': 'IsCitedBy',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/cites': 'Cites',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_supplement_to': 'IsSupplementTo',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_supplemented_by': 'IsSupplementedBy',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_continued_by': 'IsContinuedBy',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/continues': 'Continues',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/describes': 'Describes',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_described_by': 'IsDescribedBy',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/has_metadata': 'HasMetadata',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_metadata_for': 'IsMetadataFor',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/has_version': 'HasVersion',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_version_of': 'IsVersionOf',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_new_version_of': 'IsNewVersionOf',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_previous_version_of': 'IsPreviousVersionOf',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_part_of': 'IsPartOf',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/has_part': 'HasPart',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_published_in': 'IsPublishedIn',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_referenced_by': 'IsReferencedBy',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/references': 'References',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_documented_by': 'IsDocumentedBy',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/documents': 'Documents',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_compiled_by': 'IsCompiledBy',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/Compiles': 'Compiles',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_variant_form_of': 'IsVariantFormOf',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_original_form_of': 'IsOriginalFormOf',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_identical_to': 'IsIdenticalTo',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_reviewed_by': 'IsReviewedBy',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/reviews': 'Reviews',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_derived_from': 'IsDerivedFrom',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_source_of': 'IsSourceOf',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_required_by': 'IsRequiredBy',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/requires': 'Requires',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/obsoletes': 'Obsoletes',
        'https://rdmo.jochenklar.dev/terms/options/relation_type/is_obsoleted_by': 'IsObsoletedBy'
    }

    data_source_options = {
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/instrument': 'Instrument',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/media': 'Media',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/observation': 'Observation',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/trial': 'Trial',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/organism': 'Organism',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/tissue': 'Tissue',
        'https://rdmo.jochenklar.dev/terms/options/radar_data_source/other': 'Other'
    }

    def get_key(self, dict, value):
        try:
            return list(dict.keys())[list(dict.values()).index(value)]
        except ValueError:
            return None

    def check(self):
        file_type, encoding = mimetypes.guess_type(self.file_name)
        if file_type == 'application/xml':
            self.root = read_xml_file(self.file_name)
            if self.root:
                self.ns_map = get_ns_map(self.root)
                if self.root.tag == '{{{ns0}}}radarDataset'.format(**self.ns_map):
                    return True

    def process(self):
        if self.current_project is None:
            raise ValidationError(_('RADAR files can only be imported into existing projects. Please create a project first.'))

        self.catalog = self.current_project.catalog

        self.process_datasets()
        self.process_funders()

    def process_datasets(self):
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

        # title
        title_node = self.root.find('./ns1:title', self.ns_map)
        if title_node is not None:
            for attribute in [self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/title'),
                              self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/id')]:
                self.values.append(Value(
                    attribute=attribute,
                    set_index=set_index,
                    text=title_node.text
                ))

        # descriptions/description
        description_node = self.root.find("./ns1:descriptions/ns1:description[@descriptionType='Abstract']", self.ns_map)
        if description_node is not None:
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/description'),
                set_index=set_index,
                text=description_node.text
            ))

        # language
        language_node = self.root.find('./ns1:language', self.ns_map)
        if language_node is not None:
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/language'),
                set_index=set_index,
                option=self.get_option(self.get_key(self.language_options, language_node.text))
            ))

        # resourceType
        resource_type_node = self.root.find('./ns1:resourceType', self.ns_map)
        if resource_type_node is not None:
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/resource_type'),
                set_index=set_index,
                text=resource_type_node.text
            ))

            # resourceTypeGeneral
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/resource_type_general'),
                set_index=set_index,
                option=self.get_option(self.get_key(self.resource_type_general_options,
                                                    resource_type_node.attrib.get('resourceTypeGeneral', 'Dataset')))
            ))

        # subjects
        subject_nodes = self.root.findall('./ns1:subjectAreas/ns1:subjectArea/ns1:controlledSubjectAreaName', self.ns_map)
        for collection_index, subject_node in enumerate(subject_nodes):
            attribute = self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/subject')
            self.values.append(Value(
                attribute=attribute,
                set_index=set_index,
                collection_index=collection_index,
                option=self.get_option(self.get_key(self.controlled_subject_area_options, subject_node.text))
            ))

        # creators
        creator_nodes = self.root.findall('./ns1:creators/ns1:creator', self.ns_map)
        for creator_index, creator_node in enumerate(creator_nodes):
            name_node = creator_node.find('./ns1:creatorName', self.ns_map)
            if name_node is not None:
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/creator/name'),
                    set_prefix=str(set_index),
                    set_index=creator_index,
                    text=name_node.text
                ))

            name_identifier_node = creator_node.find('./ns1:nameIdentifier', self.ns_map)
            if name_identifier_node is not None:
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/creator/name_identifier'),
                    set_prefix=str(set_index),
                    set_index=creator_index,
                    text=name_identifier_node.text
                ))
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/creator/name_identifier_scheme'),
                    set_prefix=str(set_index),
                    set_index=creator_index,
                    option=self.get_option(self.get_key(self.name_identifier_scheme_options,
                                                        name_identifier_node.attrib.get('nameIdentifierScheme', 'ORCID')))
                ))

            affiliation_nodes = creator_node.findall('./ns1:affiliation', self.ns_map)
            for collection_index, affiliation_node in enumerate(affiliation_nodes):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/creator/affiliation'),
                    set_prefix=str(set_index),
                    set_index=creator_index,
                    collection_index=collection_index,
                    text=affiliation_node.text
                ))

        # contributors
        contributor_nodes = self.root.findall('./ns1:contributors/ns1:contributor', self.ns_map)
        for contributor_index, contributor_node in enumerate(contributor_nodes):
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/contributor/contributor_type'),
                set_prefix=str(set_index),
                set_index=contributor_index,
                option=self.get_option(self.get_key(self.contributor_type_options,
                                                    contributor_node.attrib.get('contributorType', 'Other')))
            ))

            name_node = contributor_node.find('./ns1:contributorName', self.ns_map)
            if name_node is not None:
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/contributor/name'),
                    set_prefix=str(set_index),
                    set_index=contributor_index,
                    text=name_node.text
                ))

            name_identifier_node = contributor_node.find('./ns1:nameIdentifier', self.ns_map)
            if name_identifier_node is not None:
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/contributor/name_identifier'),
                    set_prefix=str(set_index),
                    set_index=contributor_index,
                    text=name_identifier_node.text
                ))
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/contributor/name_identifier_scheme'),
                    set_prefix=str(set_index),
                    set_index=contributor_index,
                    option=self.get_option(self.get_key(self.name_identifier_scheme_options,
                                                        name_identifier_node.attrib.get('nameIdentifierScheme', 'ORCID')))
                ))

            affiliation_nodes = contributor_node.findall('./ns1:affiliation', self.ns_map)
            for collection_index, affiliation_node in enumerate(affiliation_nodes):
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/contributor/affiliation'),
                    set_prefix=str(set_index),
                    set_index=contributor_index,
                    collection_index=collection_index,
                    text=affiliation_node.text
                ))

        # identifier
        identifier_node = self.root.find('./ns1:identifier', self.ns_map)
        if identifier_node is not None:
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/identifier'),
                set_index=set_index,
                text=identifier_node.text
            ))

            # identifierType
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/identifier_type'),
                set_index=set_index,
                option=self.get_option(self.get_key(self.identifier_type_options,
                                                    identifier_node.attrib.get('identifierType', 'DOI')))
            ))

        # publisher
        publisher_node = self.root.find('./ns1:publisher', self.ns_map)
        if publisher_node is not None:
            attribute = \
                self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/publisher') or \
                self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/preservation/repository')
            self.values.append(Value(
                attribute=attribute,
                set_index=set_index,
                text=publisher_node.text
            ))

        # productionYear
        production_year_node = self.root.find('./ns1:productionYear', self.ns_map)
        if production_year_node is not None:
            attribute = \
                self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/created')
            self.values.append(Value(
                attribute=attribute,
                set_index=set_index,
                text=production_year_node.text,
                value_type=VALUE_TYPE_DATETIME
            ))

        # publicationYear
        publication_year_node = self.root.find('./ns1:publicationYear', self.ns_map)
        if publication_year_node is not None:
            attribute = \
                self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/issued') or \
                self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/data_publication_date')
            self.values.append(Value(
                attribute=attribute,
                set_index=set_index,
                text=publication_year_node.text,
                value_type=VALUE_TYPE_DATETIME
            ))

        # rights
        rights_nodes = self.root.findall("./ns1:rights/ns1:controlledRights", self.ns_map)
        for collection_index, rights_node in enumerate(rights_nodes):
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/sharing/conditions'),
                set_index=set_index,
                collection_index=collection_index,
                option=self.get_option(self.get_key(self.controlled_rights_options, rights_node.text))
            ))

        # rights
        rights_holder_nodes = self.root.findall("./ns1:rightsHolders/ns1:rightsHolder", self.ns_map)
        for collection_index, rights_holder_node in enumerate(rights_holder_nodes):
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/sharing/rights_holder'),
                set_index=set_index,
                collection_index=collection_index,
                text=rights_holder_node.text
            ))

        # alternate identifiers
        alternate_identifiers_nodes = self.root.findall("./ns1:alternateIdentifiers/ns1:alternateIdentifier", self.ns_map)
        for alternate_identifier_index, alternate_identifier_node in enumerate(alternate_identifiers_nodes):
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/alternate_identifier/identifier_type'),
                set_prefix=str(set_index),
                set_index=alternate_identifier_index,
                option=self.get_option(self.get_key(self.identifier_type_options,
                                                    alternate_identifier_node.attrib.get('alternateIdentifierType', 'DOI')))
            ))
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/alternate_identifier/identifier'),
                set_prefix=str(set_index),
                set_index=alternate_identifier_index,
                text=alternate_identifier_node.text
            ))

        # related identifiers
        related_identifiers_nodes = self.root.findall("./ns1:relatedIdentifiers/ns1:relatedIdentifier", self.ns_map)
        for related_identifier_index, related_identifier_node in enumerate(related_identifiers_nodes):
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/related_identifier/identifier_type'),
                set_prefix=str(set_index),
                set_index=related_identifier_index,
                option=self.get_option(self.get_key(self.identifier_type_options,
                                                    related_identifier_node.attrib.get('relatedIdentifierType', 'DOI')))
            ))
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/related_identifier/relation_type'),
                set_prefix=str(set_index),
                set_index=related_identifier_index,
                option=self.get_option(self.get_key(self.relation_type_options,
                                                    related_identifier_node.attrib.get('relationType', 'References')))
            ))
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/related_identifier/identifier'),
                set_prefix=str(set_index),
                set_index=related_identifier_index,
                text=related_identifier_node.text
            ))

        # rights
        data_source_nodes = self.root.findall("./ns1:dataSources/ns1:dataSource", self.ns_map)
        for collection_index, data_source_node in enumerate(data_source_nodes):
            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/data_source'),
                set_index=set_index,
                collection_index=collection_index,
                text=data_source_node.text
            ))

            self.values.append(Value(
                attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/dataset/data_source_detail'),
                set_index=set_index,
                collection_index=collection_index,
                option=self.get_option(self.get_key(self.data_source_options,
                                                    data_source_node.attrib.get('dataSourceDetail', 'Other')))
            ))

    def process_funders(self):
        # get existing datasets
        current_funders = self.current_project.values.filter(
            snapshot=None,
            attribute__path='project/funder/id'
        )

        # get maximum set_index to only append funders
        try:
            set_index = max([d.set_index for d in current_funders]) + 1
        except ValueError:
            set_index = 0

        funding_reference_nodes = self.root.findall("./ns1:fundingReferences/ns1:fundingReference", self.ns_map)
        print(funding_reference_nodes)
        for funding_reference_node in funding_reference_nodes:
            name_node = funding_reference_node.find('./ns1:funderName', self.ns_map)
            if name_node is not None:
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/funder/id'),
                    set_index=set_index,
                    text=name_node.text
                ))
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/funder/name'),
                    set_index=set_index,
                    text=name_node.text
                ))

            name_identifier_node = funding_reference_node.find('./ns1:funderIdentifier', self.ns_map)
            if name_identifier_node is not None:
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/funder/name_identifier'),
                    set_index=set_index,
                    text=name_identifier_node.text
                ))
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/funder/name_identifier_scheme'),
                    set_index=set_index,
                    option=self.get_option(self.get_key(self.name_identifier_scheme_options,
                                                        name_identifier_node.attrib.get('funderIdentifierType', 'ORCID')))
                ))

            award_number_node = funding_reference_node.find('./ns1:awardNumber', self.ns_map)
            if award_number_node is not None:
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/funder/programme/number'),
                    set_index=set_index,
                    text=award_number_node.text
                ))
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/funder/programme/url'),
                    set_index=set_index,
                    text=award_number_node.attrib.get('awardURI')
                ))

            award_title_node = funding_reference_node.find('./ns1:awardTitle', self.ns_map)
            if award_title_node is not None:
                self.values.append(Value(
                    attribute=self.get_attribute('https://rdmorganiser.github.io/terms/domain/project/funder/programme/title'),
                    set_index=set_index,
                    text=award_title_node.text
                ))

            # incement set_inde for the next funding reference
            set_index += 1
