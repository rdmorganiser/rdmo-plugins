# rdmo-plugins

<!--- mdtoc: toc begin -->

1. [Synopsis](#synopsis)
2. [Setup](#setup)
3. [Other plugins](#other-plugins)
   1. [RDMO Sensor AWI optionset plugin](#rdmo-sensor-awi-optionset-plugin)<!--- mdtoc: toc end -->

## Synopsis

Import and export plugins for [RDMO](https://github.com/rdmorganiser/rdmo). Included are plugins for [maDMP](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard), [DataCite (Kernel 4.3)](https://schema.datacite.org/meta/kernel-4.3/), and the [Radar metadata schema](https://www.radar-service.eu/de/radar-schema).

**Since the RDMO questionaires and the domain does not contain all information needed for maDMP, DataCite, or Radar, the exports will not produce valid files. We will fix this in the future.**

Please visit the [RDMO documentation](https://rdmo.readthedocs.io/en/latest/plugins/index.html#project-export-plugins) for detailed information.

Please note that the re3data plugin was moved to a [seperate repository](https://github.com/rdmorganiser/rdmo-re3data).

## Setup

Install the plugins in your RDMO virtual environment using pip (directly from GitHub):

```bash
pip install git+https://github.com/rdmorganiser/rdmo-plugins
```

Add the `rdmo_plugins` to the `INSTALLED_APPS` in `config/settings/local.py`:

```python
from . import INSTALLED_APPS
INSTALLED_APPS = ['rdmo_plugins'] + INSTALLED_APPS
```

Add the export plugins to the `PROJECT_EXPORTS` in `config/settings/local.py`:

```python
from django.utils.translation import ugettext_lazy as _
from . import PROJECT_EXPORTS

PROJECT_EXPORTS += [
    ('madmp', _('as maDMP JSON'), 'rdmo_plugins.exports.madmp.MaDMPExport'),
    ('datacite-xml', _('as DataCite XML'), 'rdmo_plugins.exports.datacite.DataCiteExport'),
    ('radar-xml', _('as RADAR XML'), 'rdmo_plugins.exports.radar.RadarExport'),
    ('radar', _('directly to RADAR'), 'rdmo_plugins.exports.radar.RadarExportProvider'),
    ('zenodo', _('directly to Zenodo'), 'rdmo_plugins.exports.zenodo.ZenodoExportProvider')
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

## Other plugins

### RDMO Sensor AWI optionset plugin

[https://github.com/hafu/rdmo-sensor-awi](https://github.com/hafu/rdmo-sensor-awi)

Queries the Sensor Information System of the Alfred-Wegener-Institut, Helmholtz-Zentrum für Polar- und Meeresforschung (AWI).

This is an example optionset plugin, to show how to gather information from other systems.
