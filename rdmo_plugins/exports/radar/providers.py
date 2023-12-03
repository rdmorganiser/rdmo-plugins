import time

from django import forms
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from rdmo.domain.models import Attribute
from rdmo.projects.models import Value
from rdmo.services.providers import OauthProviderMixin

from .exports import RadarExport


class RadarExportProvider(RadarExport, OauthProviderMixin):

    other = 'OTHER'

    abstract = 'ABSTRACT'

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
        'name_identifier_scheme/ror': 'ROR',
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
        'contributor_type/sponsor': 'SPONSOR',
        'contributor_type/supervisor': 'SUPERVISOR',
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
        'radar_controlled_subject_area/computer_science': 'COMPUTER_SCIENCE',
        'radar_controlled_subject_area/economics': 'ECONOMICS',
        'radar_controlled_subject_area/engineering': 'ENGINEERING',
        'radar_controlled_subject_area/environmental_science_and_ecology': 'ENVIRONMENTAL_SCIENCE_AND_ECOLOGY',
        'radar_controlled_subject_area/ethnology': 'ETHNOLOGY',
        'radar_controlled_subject_area/geological_science': 'GEOLOGICAL_SCIENCE',
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
        'relation_type/describes': 'DESCRIBES',
        'relation_type/is_described_by': 'IS_DESCRIBED_BY',
        'relation_type/has_metadata': 'HAS_METADATA',
        'relation_type/is_metadata_for': 'IS_METADATA_FOR',
        'relation_type/has_version': 'HAS_VERSION',
        'relation_type/is_version_of': 'IS_VERSION_OF',
        'relation_type/is_new_version_of': 'IS_NEW_VERSION_OF',
        'relation_type/is_previous_version_of': 'IS_PREVIOUS_VERSION_OF',
        'relation_type/is_part_of': 'IS_PART_OF',
        'relation_type/has_part': 'HAS_PART',
        'relation_type/is_published_in': 'IS_PUBLISHED_IN',
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
        'relation_type/requires': 'REQUIRES',
        'relation_type/is_required_by': 'IS_REQUIRED_BY',
        'relation_type/obsoletes': 'OBSOLETES',
        'relation_type/is_obsoleted_by': 'IS_OBSOLETED_BY'
    }

    class Form(forms.Form):

        dataset = forms.CharField(label=_('Select dataset of your project'))
        workspace = forms.CharField(label=_('Select a workspace in RADAR'))

        def __init__(self, *args, **kwargs):
            dataset_choices = kwargs.pop('dataset_choices')
            workspace_choices = kwargs.pop('workspace_choices')
            radar_urls = kwargs.pop('radar_urls')

            super().__init__(*args, **kwargs)

            dataset_choices_with_radar_urls = []
            for dataset, radar_url in zip(dataset_choices, radar_urls):
                set_index, label = dataset
                if radar_url is not None:
                    label += f' (Already exported to RADAR: <a href="{radar_url}" target="_blank">{radar_url}</a>)'
                dataset_choices_with_radar_urls.append((set_index, mark_safe(label)))

            self.fields['dataset'].widget = forms.RadioSelect(choices=dataset_choices_with_radar_urls)
            self.fields['workspace'].widget = forms.RadioSelect(choices=workspace_choices)

    def render(self):
        datasets = self.get_set('project/dataset/id')
        dataset_choices = [(dataset.set_index, dataset.value) for dataset in datasets]
        radar_urls = [self.get_text('project/dataset/radar_url', set_index=dataset.set_index) for dataset in datasets]

        self.store_in_session(self.request, 'dataset_choices', dataset_choices)
        self.store_in_session(self.request, 'radar_urls', radar_urls)
        self.store_in_session(self.request, 'project_id', self.project.id)

        if self.pop_from_session(self.request, 'get') is True:
            workspace_choices = self.get_from_session(self.request, 'workspace_choices')
            form = self.Form(
                dataset_choices=dataset_choices,
                workspace_choices=workspace_choices,
                radar_urls=radar_urls
            )
            return render(self.request, 'plugins/exports_radar.html', {'form': form}, status=200)
        else:
            # run the oauth get request to obtain the workspace_choices
            url = self.get_get_url()
            return self.get(self.request, url)

    def submit(self):
        dataset_choices = self.get_from_session(self.request, 'dataset_choices')
        workspace_choices = self.get_from_session(self.request, 'workspace_choices')
        radar_urls = self.get_from_session(self.request, 'radar_urls')

        form = self.Form(
            self.request.POST,
            dataset_choices=dataset_choices,
            workspace_choices=workspace_choices,
            radar_urls=radar_urls
        )

        if 'cancel' in self.request.POST:
            return redirect('project', self.project.id)

        if form.is_valid():
            self.store_in_session(self.request, 'set_index', form.cleaned_data['dataset'])

            url = self.get_post_url(form.cleaned_data['workspace'])
            data = self.get_post_data(form.cleaned_data['dataset'])
            return self.post(self.request, url, data)
        else:
            return render(self.request, 'plugins/exports_radar.html', {'form': form}, status=200)

    def get_get_url(self):
        return f'{self.radar_url}/radar/api/workspaces'

    def get_success(self, request, response):
        workspace_choices = [
            (workspace.get('id'), workspace.get('descriptiveMetadata', {}).get('title'))
            for workspace in response.json().get('data', [])
        ]
        self.store_in_session(request, 'get', True)
        self.store_in_session(request, 'workspace_choices', workspace_choices)
        return redirect('project_export', self.get_from_session(request, 'project_id'), self.key)

    def get_post_url(self, workspace_id):
        return f'{self.radar_url}/radar/api/workspaces/{workspace_id}/datasets'

    def get_post_data(self, set_index):
        now = int(time.time())
        email = self.request.user.email
        dataset = self.get_dataset(set_index)

        return {
            'technicalMetadata': {
                "retentionPeriod": 10,
                "archiveDate": now,
                "publishDate": now,
                "responsibleEmail": email,
                "schema": {
                    "key": "RDDM",
                    "version": "9.1"
                }
            },
            'descriptiveMetadata': dataset
        }

    def post_success(self, request, response):
        radar_id = response.json().get('id')
        if radar_id:
            project_id = self.get_from_session(self.request, 'project_id')
            set_index = self.get_from_session(self.request, 'set_index')

            if request.LANGUAGE_CODE == 'de':
                radar_url = f'{self.radar_url}/radar/de/dataset/{radar_id}'
            else:
                radar_url = f'{self.radar_url}/radar/en/dataset/{radar_id}'

            try:
                attribute = Attribute.objects.get(path='project/dataset/radar_id')
                value, created = Value.objects.get_or_create(
                    attribute=attribute,
                    project_id=project_id,
                    set_index=set_index
                )
                value.text = radar_id
                value.save()
            except Attribute.DoesNotExist:
                pass

            try:
                attribute = Attribute.objects.get(path='project/dataset/radar_url')
                value, created = Value.objects.get_or_create(
                    attribute=attribute,
                    project_id=project_id,
                    set_index=set_index
                )
                value.text = radar_url
                value.save()
            except Attribute.DoesNotExist:
                pass

            return redirect(radar_url)
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
        return f'{self.radar_url}/radar-backend/oauth/authorize'

    @property
    def token_url(self):
        return f'{self.radar_url}/radar-backend/oauth/token'

    @property
    def client_id(self):
        return settings.RADAR_PROVIDER['client_id']

    @property
    def client_secret(self):
        return settings.RADAR_PROVIDER['client_secret']

    @property
    def redirect_uri(self):
        return settings.RADAR_PROVIDER['redirect_uri']

    def get_authorize_params(self, request, state):
        return {
            'response_type': 'code',
            'client_id': 'jochenklar',
            'redirect_uri': self.redirect_uri,
            'state': state
        }

    def get_callback_params(self, request):
        return {
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'code': request.GET.get('code')
        }

    def get_callback_auth(self, request):
        return (self.client_id, self.client_secret)

    def get_error_message(self, response):
        return response.json().get('exception')
