import logging
from urllib.parse import urlencode

import requests
from rdmo.core.xml import parse_xml_string
from rdmo.domain.models import Attribute
from rdmo.options.providers import Provider

logger = logging.getLogger(__name__)


class Re3DataProvider(Provider):

    re3data_url = 'https://www.re3data.org/api/beta/repositories'

    subject_attribute = 'https://rdmorganiser.github.io/terms/domain/project/research_field/title'

    # create mapping of RDMO research field identifiers to DFG subject areas (Fachkollegien)
    subjects = {
        'https://rdmorganiser.github.io/terms/options/research_fields/169': '101 Ancient Cultures',
        'https://rdmorganiser.github.io/terms/options/research_fields/174': '102 History',
        'https://rdmorganiser.github.io/terms/options/research_fields/171': '103 Fine Arts, Music, Theatre and Media Studies',
        'https://rdmorganiser.github.io/terms/options/research_fields/173': '104 Linguistics',
        'https://rdmorganiser.github.io/terms/options/research_fields/170': '105 Literary Studies',
        'https://rdmorganiser.github.io/terms/options/research_fields/172': '106 Non-European Languages and Cultures, Social and Cultural Anthropology, Jewish Studies and Religious Studies',
        'https://rdmorganiser.github.io/terms/options/research_fields/175': '107 Theology',
        'https://rdmorganiser.github.io/terms/options/research_fields/176': '108 Philosophy',
        'https://rdmorganiser.github.io/terms/options/research_fields/178': '109 Education Sciences',
        'https://rdmorganiser.github.io/terms/options/research_fields/177': '110 Psychology',
        'https://rdmorganiser.github.io/terms/options/research_fields/179': '111 Social Sciences',
        'https://rdmorganiser.github.io/terms/options/research_fields/180': '112 Economics',
        'https://rdmorganiser.github.io/terms/options/research_fields/181': '113 Jurisprudence',
        'https://rdmorganiser.github.io/terms/options/research_fields/182': '201 Basic Biological and Medical Research',
        'https://rdmorganiser.github.io/terms/options/research_fields/183': '202 Plant Sciences',
        'https://rdmorganiser.github.io/terms/options/research_fields/186': '203 Zoology',
        'https://rdmorganiser.github.io/terms/options/research_fields/184': '204 Microbiology, Virology and Immunology',
        'https://rdmorganiser.github.io/terms/options/research_fields/185': '205 Medicine',
        'https://rdmorganiser.github.io/terms/options/research_fields/187': '206 Neurosciences',
        'https://rdmorganiser.github.io/terms/options/research_fields/188': '207 Agriculture, Forestry, Horticulture and Veterinary Medicine',
        'https://rdmorganiser.github.io/terms/options/research_fields/189': '301 Molecular Chemistry',
        'https://rdmorganiser.github.io/terms/options/research_fields/192': '302 Chemical Solid State and Surface Research',
        'https://rdmorganiser.github.io/terms/options/research_fields/190': '303 Physical and Theoretical Chemistry',
        'https://rdmorganiser.github.io/terms/options/research_fields/191': '304 Analytical Chemistry, Method Development (Chemistry)',
        'https://rdmorganiser.github.io/terms/options/research_fields/193': '305 Biological Chemistry and Food Chemistry',
        'https://rdmorganiser.github.io/terms/options/research_fields/194': '306 Polymer Research',
        'https://rdmorganiser.github.io/terms/options/research_fields/195': '307 Condensed Matter Physics',
        'https://rdmorganiser.github.io/terms/options/research_fields/196': '308 Optics, Quantum Optics and Physics of Atoms, Molecules and Plasmas',
        'https://rdmorganiser.github.io/terms/options/research_fields/198': '309 Particles, Nuclei and Fields',
        'https://rdmorganiser.github.io/terms/options/research_fields/197': '310 Statistical Physics, Soft Matter, Biological Physics, Nonlinear Dynamics',
        'https://rdmorganiser.github.io/terms/options/research_fields/199': '311 Astrophysics and Astronomy',
        'https://rdmorganiser.github.io/terms/options/research_fields/200': '312 Mathematics',
        'https://rdmorganiser.github.io/terms/options/research_fields/201': '313 Atmospheric Science and Oceanography',
        'https://rdmorganiser.github.io/terms/options/research_fields/202': '314 Geology and Palaeontology',
        'https://rdmorganiser.github.io/terms/options/research_fields/203': '315 Geophysics and Geodesy',
        'https://rdmorganiser.github.io/terms/options/research_fields/204': '316 Geochemistry, Mineralogy and Crystallography',
        'https://rdmorganiser.github.io/terms/options/research_fields/206': '317 Geography',
        'https://rdmorganiser.github.io/terms/options/research_fields/205': '318 Water Research',
        'https://rdmorganiser.github.io/terms/options/research_fields/207': '401 Production Technology',
        'https://rdmorganiser.github.io/terms/options/research_fields/208': '402 Mechanics and Constructive Mechanical Engineering',
        'https://rdmorganiser.github.io/terms/options/research_fields/209': '403 Process Engineering, Technical Chemistry',
        'https://rdmorganiser.github.io/terms/options/research_fields/210': '404 Heat Energy Technology, Thermal Machines, Fluid Mechanics',
        'https://rdmorganiser.github.io/terms/options/research_fields/211': '405 Materials Engineering',
        'https://rdmorganiser.github.io/terms/options/research_fields/212': '406 Materials Science',
        'https://rdmorganiser.github.io/terms/options/research_fields/213': '407 Systems Engineering',
        'https://rdmorganiser.github.io/terms/options/research_fields/214': '408 Electrical Engineering',
        'https://rdmorganiser.github.io/terms/options/research_fields/215': '409 Computer Science',
        'https://rdmorganiser.github.io/terms/options/research_fields/216': '410 Construction Engineering and Architecture'
    }

    def get_options(self, project):
        options = []

        # get the attribute for the subjects
        try:
            subject_attribute = Attribute.objects.get(uri=self.subject_attribute)
        except Attribute.DoesNotExist:
            return {}

        # get current values for the subject attribute
        values = project.values.filter(snapshot=None, attribute=subject_attribute)

        # get subjects from the values
        subjects = []
        for value in values:
            if value.option is not None:
                subject = self.subjects.get(value.option.uri)
                if subject:
                    subjects.append(subject)

        if subjects:
            # construct re3data url
            url = self.re3data_url + '?' + '&'.join([
                urlencode({'subjects[]': subject}) for subject in subjects
            ])

            # perform http request
            logger.debug('Requesting %s', url)
            response = requests.get(url)
            try:
                response.raise_for_status()

            except requests.exceptions.HTTPError:
                return {}

            # parse xml string and get list of repositories
            xml = parse_xml_string(response.content.decode())
            if xml is None:
                return {}

            # loop over repository list
            for repository_node in xml.findall('repository'):
                options.append({
                    'external_id': repository_node.find('id').text,
                    'text': repository_node.find('name').text
                })

        return options
