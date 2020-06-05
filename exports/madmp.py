import json
from collections import defaultdict

from django.http import HttpResponse

from rdmo.projects.exports import Export


class MaDMPExport(Export):

    currency_codes = [
        "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
        "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL",
        "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY",
        "COP", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD",
        "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GGP", "GHS",
        "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF",
        "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD",
        "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT",
        "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD",
        "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN",
        "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK",
        "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR",
        "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL", "SOS", "SPL*","SRD",
        "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY",
        "TTD", "TVD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VEF",
        "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR",
        "ZMW", "ZWD"
    ]

    languages = {
        'en': 'eng',
        'de': 'deu'
    }

    data_access_options = {
        'dataset_sharing_options/69 ': 'open',
        'dataset_sharing_options/68': 'shared',
        'dataset_sharing_options/67': 'shared',
        'dataset_sharing_options/70': 'closed'
    }

    certified_with_options = {
        # '': 'din31644',
        # '': 'dini-zertifikat',
        # '': 'dsa',
        # '': 'iso16363',
        # '': 'iso16919',
        # '': 'trac',
        # '': 'wds',
        # '': 'coretrustseal'
    }

    pid_system_options = {
        'pid_types/124': 'ark',
        # '': 'arxiv',
        # '': 'bibcode',
        'pid_types/123': 'doi',
        # '': 'ean13',
        # '': 'eissn',
        # '': 'handle',
        # '': 'igsn',
        # '': 'isbn',
        # '': 'issn',
        # '': 'istc',
        # '': 'lissn',
        # '': 'lsid',
        # '': 'pmid',
        'pid_types/122': 'purl',
        # '': 'upc',
        # '': 'url',
        'pid_types/120': 'urn',
        'pid_types/154': 'other',
        'pid_types/121': 'other'
    }

    license_ref_options = {
        'dataset_license_types/71': 'https://creativecommons.org/licenses/by/4.0/',
        'dataset_license_types/73': 'https://creativecommons.org/licenses/by-nc/4.0/',
        'dataset_license_types/74': 'https://creativecommons.org/licenses/by-nd/4.0/',
        'dataset_license_types/75': 'https://creativecommons.org/licenses/by-sa/4.0/',
        'dataset_license_types/cc0': 'https://creativecommons.org/publicdomain/zero/1.0/deed.de'
    }

    person_id_type_options = {
        # '': 'orcid',
        # '': 'isni',
        # '': 'openid',
        # '': 'other'
    }

    dataset_id_type_options = {
        # '': 'handle',
        # '': 'doi',
        # '': 'ark',
        # '': 'url',
        # '': 'other'
    }

    dmp_id_type_options = {
        # '': 'handle',
        # '': 'doi',
        # '': 'ark',
        # '': 'url',
        # '': 'other'
    }

    funder_id_type_options = {
        # '': 'fundref',
        # '': 'url',
        # '': 'other'
    }

    grant_id_type_options = {
        # '': 'url',
        # '': 'other'
    }

    metadata_standard_id_options = {
        # '': 'url',
        # '': 'other'
    }

    yes_no_unknown = {
        True: 'yes',
        False: 'no',
        None: 'unknown'
    }

    def render(self):
        response = HttpResponse(json.dumps({
            'dmp': self.get_dmp()
        }, indent=2), content_type='application/json')
        response['Content-Disposition'] = 'filename="%s.json"' % self.project.title
        return response

    def get_dmp(self):
        # dmp/title, dmp/created, dmp/modified, dmp/language
        dmp = defaultdict(list)
        dmp.update({
            'title': 'maDMP for {}'.format(self.project.title),
            'created': self.project.created.isoformat(),
            'modified': self.project.updated.isoformat(),
            'language': self.languages['en']
            # 'language': self.languages[self.project.language]
        })

        # dmp/contact
        contact = self.get_person('project/dmp/contact/name')
        if contact:
            dmp['contact'] = contact

        # dmp/contributor
        for partner in self.get_set('project/partner/id'):
            role = 'Contact person for {}'.format(partner.text)
            contributor = self.get_person('project/partner/contact_person', set_index=partner.set_index, roles=[role])
            if contributor:
                dmp['contributor'].append(contributor)

        for dataset in self.get_set('project/dataset/id'):
            for role, attribute in [
                ('Responsible for backup for {}'.format(dataset.text), 'project/dataset/data_security/backup_responsible'),
                ('Responsible for metadata for {}'.format(dataset.text), 'project/dataset/metadata/responsible_person'),
                ('Responsible for PIDs for {}'.format(dataset.text), 'project/dataset/pids/responsible_person'),
            ]:
                contributor = self.get_person(attribute, set_index=dataset.set_index, roles=[role])
                if contributor:
                    dmp['contributor'].append(contributor)

        contributor = self.get_person('project/preservation/responsible_person', set_index=dataset.set_index, roles=['Responsible for preservation'])
        if contributor:
            dmp['contributor'].append(contributor)

        # dmp/cost
        for title, attribute in [
            ('Personal costs for data creation', 'project/costs/creation/personnel'),
            ('Non personal costs for data creation', 'project/costs/creation/non_personnel'),
            ('Personal costs for data usage', 'project/costs/usage/personnel'),
            ('Non personal costs for data creation', 'project/costs/usage/non_personnel'),
            ('Personal costs for data storage', 'project/costs/storage/personnel'),
            ('Non personal costs for data storage', 'project/costs/storage/non_personnel'),
            ('Personal costs for metadata curation', 'project/costs/metadata/personnel'),
            ('Non personal costs for metadata curation', 'project/costs/metadata/non_personnel'),
            ('Personal costs for PID curation', 'project/costs/pid/personnel'),
            ('Non personal costs for PID curation', 'project/costs/pid/non_personnel'),
            ('Personal costs for data anonymization', 'project/costs/sensitive_data/anonymization/personnel'),
            ('Non personal costs for data anonymization', 'project/costs/sensitive_data/anonymization/non_personnel'),
            ('Personal costs for data security', 'project/costs/sensitive_data/security/personnel'),
            ('Non personal costs  for data security', 'project/costs/sensitive_data/security/non_personnel'),
            ('Personal costs for interlectual property rights', 'project/costs/ipr/personnel'),
            ('Non personal costs for interlectual property rights', 'project/costs/ipr/non_personnel'),
            ('Personal costs for preservation', 'project/costs/preservation/personnel'),
            ('Non personal costs for preservation', 'project/costs/preservation/non_personnel')
        ]:
            cost = self.get_cost(title, attribute)
            if cost:
                dmp['cost'].append(cost)

        # dmp/dataset
        for dataset in self.get_set('project/dataset/id'):
            dmp_dataset = self.get_dataset(dataset)
            if dmp_dataset:
                dmp['dataset'].append(dmp_dataset)

        # dmp/dmp_id
        dmp_id = self.get_text('project/dmp/identifier')
        if dmp_id:
            contributor['dmp_id'] = {
                'identifier': dmp_id,
                'type': self.get_option(self.dmp_id_type_option, 'project/dmp/identifier_type', default='other')
            }

        # dmp/dataset/ethical_issues_description

        # dmp/project
        dmp['project'] = [
            {
                'title': self.project.title,
                'description': self.project.description,
                'start': self.get_timestamp('project/schedule/project_start'),
                'end': self.get_timestamp('project/schedule/project_end')
            }
        ]

        return dmp

    def get_person(self, attribute, set_index=0, roles=None):
        name = self.get_text(attribute + '/name', set_index=set_index)
        if name:
            contributor = {
                'name': name
            }

            mbox = self.get_text(attribute + '/mbox', set_index=set_index)
            if mbox:
                contributor['mbox'] = mbox

            identifier = self.get_text(attribute + '/identifier', set_index=set_index)
            if identifier:
                contributor['contributor_id'] = {
                    'identifier': identifier,
                    'type': self.get_option(self.person_id_type_options, attribute + '/identifier_type', set_index=set_index, default='other')
                }

            if roles:
                contributor['role'] = roles

            return contributor
        else:
            return None

    def get_cost(self, title, attribute):
        value = self.get_value(attribute)
        if value:
            cost = {
                'title': title
            }

            try:
                cost['value'] = int(value.text)
            except ValueError:
                try:
                    cost['value'] = float(value.text)
                except ValueError:
                    cost['value'] = 0

            if value.unit:
                cost['description'] = '{} in {}'.format(title, value.unit)

            # this is a hack to make 'Euro' work
            if value.unit.upper()[:3] in self.currency_codes:
                cost['currency_code'] = value.unit.upper()[:3]

            return cost
        else:
            return None

    def get_dataset(self, dataset):
        dmp_dataset = defaultdict(list)

        # dmp/dataset/title
        dmp_dataset['title'] = self.get_text('project/dataset/id', dataset.set_index) or 'Dataset #{}'.format(dataset.set_index + 1)

        # dmp/dataset/description
        description = self.get_text('project/dataset/description', dataset.set_index)
        if description:
            dmp_dataset['description'] = description

        # dmp/dataset/quality_assurance
        data_quality_assurance = self.get_list('project/dataset/quality_assurance', dataset.set_index)
        if data_quality_assurance:
            dmp_dataset['data_quality_assurance'] = data_quality_assurance

        # dmp/dataset/identifier
        dataset_identifier = self.get_text('project/dataset/dataset_identifier', dataset.set_index)
        if dataset_identifier:
            dmp_dataset['dataset_id'] = {
                'identifier': dataset_identifier,
                'type': self.get_option(self.dataset_id_type_options, 'project/dataset/dataset_identifier', set_index=dataset.set_index, default='other')
            }
        else:
            dmp_dataset['dataset_id'] = {
                'identifier': self.get_text('project/dataset/id', dataset.set_index),
                'type': 'other'
            }

        # distribution during the project
        distribution_during = {}

        # dmp/dataset/distribution/access_url
        access_url = self.get_text('project/dataset/storage/uri', dataset.set_index)
        if access_url:
            distribution_during['access_url'] = access_url

        # dmp/dataset/distribution/data_access
        data_access = self.get_option(self.data_access_options, 'project/dataset/sharing/yesno', set_index=dataset.set_index)
        if data_access:
            distribution_during['data_access'] = data_access

        # dmp/dataset/distribution/format
        dmp_format = self.get_list('project/dataset/format', dataset.set_index)
        if dmp_format:
            distribution_during['format'] = dmp_format

        if distribution_during:
            dmp_dataset['distribution'].append({
                'title': 'Storage during the project',
                **distribution_during
            })

        # dmp/dataset/distribution (after the project)
        distribution_after = {}

        # dmp/dataset/distribution/data_access
        distribution_after['data_access'] = 'open' if (distribution_during['data_access'] == 'open') else 'closed'

        # dmp/dataset/distribution/certified_with
        certified_with = self.get_option(self.certified_with_options, 'project/dataset/preservation/certification', dataset.set_index)
        if certified_with:
            distribution_after['certified_with'] = certified_with

        # dmp/dataset/distribution/pid_system
        pid_system = self.get_option(self.pid_system_options, 'project/dataset/pids/system', dataset.set_index)
        if pid_system:
            distribution_after['pid_system'] = pid_system

        # dmp/dataset/distribution/host
        host_title = self.get_value('project/dataset/preservation/repository', dataset.set_index)
        if host_title:
            distribution_after['host'] = {
                'title': host_title.value
            }

        # dmp/dataset/distribution/license_ref
        license_ref = self.get_option(self.license_ref_options, 'project/dataset/sharing/conditions', dataset.set_index)
        if license_ref:
            license = {
                'license_ref': license_ref
            }

            start_date = self.get_timestamp('project/dataset/data_publication_date', dataset.set_index)
            if start_date:
                license['start_date'] = start_date

            distribution_after['license'] = [license]

        if distribution_after:
            dmp_dataset['distribution'].append({
                'title': 'Preservation after the project',
                **distribution_after
            })

        # dmp/dataset/issued
        issued = self.get_timestamp('project/dataset/data_publication_date', dataset.set_index)
        if issued:
            dmp_dataset['issued'] = issued

        # dmp/dataset/keywords
        keywords = self.get_list('project/research_question/keywords')
        if keywords:
            dmp_dataset['keyword'] = keywords

        # dmp/dataset/personal_data
        personal_data = self.get_bool('project/dataset/sensitive_data/personal_data_yesno/yesno', dataset.set_index)
        dmp_dataset['personal_data'] = self.yes_no_unknown[personal_data]

        # dmp/dataset/preservation_statement
        preservation_statement = self.get_text('project/dataset/preservation/purpose', dataset.set_index)
        if preservation_statement:
            dmp_dataset['preservation_statement'] = preservation_statement

        # dmp/dataset/security_and_privacy
        for title, attribute in [
            ('Access permissions', 'project/dataset/data_security/access_permissions'),
            ('Security measures', 'project/dataset/data_security/security_measures')
        ]:
            value = self.get_value(attribute)
            if value:
                dmp_dataset['security_and_privacy'].append({
                    'title': title,
                    'description': value.text
                })

        # dmp/dataset/sensitive_data
        sensitive_data = self.get_bool('project/dataset/sensitive_data/personal_data/bdsg_3_9', dataset.set_index)
        dmp_dataset['sensitive_data'] = self.yes_no_unknown[sensitive_data]

        # dmp/dataset/type
        dmp_type = self.get_text('project/dataset/type', dataset.set_index)
        if dmp_type:
            dmp_dataset['type'] = dmp_type

        return dmp_dataset
