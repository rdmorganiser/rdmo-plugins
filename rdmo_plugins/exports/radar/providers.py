import time

from django import forms
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from rdmo.domain.models import Attribute
from rdmo.projects.exports import Export
from rdmo.projects.models import Value
from rdmo.services.providers import OauthProviderMixin

from .mixins import RadarMixin


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

    def render(self):
        datasets = self.get_set('project/dataset/id')
        dataset_choices = [(dataset.set_index, dataset.value) for dataset in datasets]

        self.store_in_session(self.request, 'dataset_choices', dataset_choices)
        self.store_in_session(self.request, 'project_id', self.project.id)

        if self.pop_from_session(self.request, 'get') is True:
            workspace_choices = self.get_from_session(self.request, 'workspace_choices')
            form = self.Form(
                dataset_choices=dataset_choices,
                workspace_choices=workspace_choices
            )
            return render(self.request, 'plugins/exports_radar.html', {'form': form}, status=200)
        else:
            # run the oauth get request to obtain the workspace_choices
            url = self.get_get_url()
            return self.get(self.request, url)

    def submit(self):
        dataset_choices = self.get_from_session(self.request, 'dataset_choices')
        workspace_choices = self.get_from_session(self.request, 'workspace_choices')

        form = self.Form(
            self.request.POST,
            dataset_choices=dataset_choices,
            workspace_choices=workspace_choices
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
        return '{}/radar/api/workspaces'.format(self.radar_url)

    def get_success(self, request, response):
        workspace_choices = [
            (workspace.get('id'), workspace.get('descriptiveMetadata', {}).get('title'))
            for workspace in response.json().get('data', [])
        ]
        self.store_in_session(request, 'get', True)
        self.store_in_session(request, 'workspace_choices', workspace_choices)
        return redirect('project_export', self.get_from_session(request, 'project_id'), self.key)

    def get_post_url(self, workspace_id):
        return '{}/radar/api/workspaces/{}/datasets'.format(self.radar_url, workspace_id)

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
                    "version": "09"
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
                radar_url = '{}/radar/de/dataset/{}'.format(self.radar_url, radar_id)
            else:
                radar_url = '{}/radar/en/dataset/{}'.format(self.radar_url, radar_id)

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
