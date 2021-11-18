import zipfile

from django.http import HttpResponse

from rdmo.core.exports import prettify_xml
from rdmo.projects.exports import Export

from .mixins import RadarMixin
from .renderers import RadarExportRenderer


class RadarExport(RadarMixin, Export):

    def render(self):
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'filename="%s.zip"' % self.project.title

        zip_file = zipfile.ZipFile(response, 'w')
        for rdmo_dataset in self.get_set('project/dataset/id'):
            set_index = rdmo_dataset.set_index

            file_name = '{}.xml'.format(
                self.get_text('project/dataset/identifier', set_index=set_index) or
                self.get_text('project/dataset/id', set_index=set_index) or
                str(set_index + 1)
            )

            dataset = self.get_dataset(set_index)
            xmldata = RadarExportRenderer().render(dataset)
            zip_file.writestr(file_name, prettify_xml(xmldata))

        return response
