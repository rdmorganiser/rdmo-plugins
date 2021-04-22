rdmo-plugins
============

Import and export plugins for [RDMO](https://github.com/rdmorganiser/rdmo). Included are plugins for [maDMP](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard), [DataCite (Kernel 4.3)](https://schema.datacite.org/meta/kernel-4.3/), and the [Radar metadata schema](https://www.radar-service.eu/de/radar-schema).

**Since the RDMO questionaires and the domain does not contain all information needed for maDMP, DataCite, or Radar, the exports will not produce valid files. We will fix this in the future.**

Please visit the [RDMO documentation](https://rdmo.readthedocs.io/en/latest/configuration/plugins.html#project-export-plugins) for detailed information.

Please note that the re3data plugin was moved to a [seperate repository](https://github.com/rdmorganiser/rdmo-re3data).


Setup
-----

Install the plugins in your RDMO virtual environment using pip (directly from GitHub):

```bash
pip install git+https://github.com/rdmorganiser/rdmo-plugins
```

Add the export plugins to the `PROJECT_EXPORTS` in `config/settings/local.py`:

```python
from django.utils.translation import ugettext_lazy as _
from . import PROJECT_EXPORTS

PROJECT_EXPORTS += [
    ('madmp', _('as maDMP JSON'), 'rdmo_plugins.exports.madmp.MaDMPExport'),
    ('datacite', _('as DataCite XML'), 'rdmo_plugins.exports.datacite.DataCiteExport'),
    ('radar', _('as RADAR XML'), 'rdmo_plugins.exports.radar.RadarExport')
]
```

Add the import plugins to the `PROJECT_IMPORTS` in `config/settings/local.py`:

```python
from django.utils.translation import ugettext_lazy as _
from . import PROJECT_IMPORTS

PROJECT_IMPORTS += [
    ('madmp', _('from maDMP'), 'rdmo_plugins.imports.madmp.MaDMPImport'),
    ('datacite', _('from DataCite XML'), 'rdmo_plugins.imports.datacite.DataCiteImport'),
    ('radar', _('from RADAR XML'), 'rdmo_plugins.imports.radar.RadarImport'),
]
```

After restarting RDMO, the exports/imports should be usable for all projects.
