# RDMO Plugins

This repository contains a list of the currently available [RDMO](https://rdmorganiser.github.io/) plugins.

For additional information, please refer to the corresponding documentation at
https://rdmo.readthedocs.io/en/latest/plugins/index.html.


## Plugins maintained by RDMO

### RDMO re3data plugin

https://github.com/rdmorganiser/rdmo-plugins-re3data

The dynamic re3data optionset will query [re3data.org](https://www.re3data.org/) for repositories
that match the research field of the project (as given by the `project/research_field/title` attribute).


### RDMO ORCID plugin

https://github.com/rdmorganiser/rdmo-plugins-orcid

This plugin implements dynamic option set, that queries the expanded-search endpoint of the
[ORCID public API](https://info.orcid.org/documentation/api-tutorials/api-tutorial-searching-the-orcid-registry/).


### RDMO ROR plugin

https://github.com/rdmorganiser/rdmo-plugins-ror

This plugin implements dynamic option set, that queries the expanded-search endpoint of the
[ROR API](https://ror.readme.io/docs/rest-api).


### RDMO GND plugin

https://github.com/rdmorganiser/rdmo-plugins-gnd

This plugin implements dynamic option set, that queries the API for the Gemeinsame Normdatei (GND)
at https://lobid.org/gnd.


### RDMO Wikidata plugin

https://github.com/rdmorganiser/rdmo-plugins-wikidata

This plugin implements dynamic option set, that queries the Wikidata Search API at https://www.wikidata.org/w/api.php.


### RDMO maDMP plugin

https://github.com/rdmorganiser/rdmo-plugins-madmp

This repo contains two plugins to provide interoperability of [RDMO](https://github.com/rdmorganiser/rdmo)
with the [RDA-DMP-Common-Standard (maDMP)](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard):

* `rdmo_madmp.exports.MaDMPExport`, which lets users download their RDMO project as maDMP JSON metadata files,
* `rdmo_madmp.exports.MaDMPExport`, which lets users import maDMP JSON metadata files into RDMO.


### RDMO DataCite plugin

https://github.com/rdmorganiser/rdmo-plugins-datacite

This repo implements two plugins to provide interoperability of [RDMO](https://github.com/rdmorganiser/rdmo)
with [DataCite](https://datacite.org/):

* `rdmo_datacite.exports.DataCiteExport`, which lets users download their RDMO datasets
  as DataCite XML metadata files (combined in one ZIP file),
* `rdmo_datacite.imports.DataCiteImport`, which lets users import DataCite XML metadata
  files into an **existing** RDMO project.


### RDMO RADAR plugin

https://github.com/rdmorganiser/rdmo-plugins-radar

This repo implements several plugins to connect [RDMO](https://github.com/rdmorganiser/rdmo)
with [RADAR](https://www.radar-service.eu/):

* `rdmo_radar.exports.RadarExport`, which lets users download their RDMO datasets as RADAR-XML metadata files,
* `rdmo_radar.exports.RadarExportProvider`, which lets push their RDMO datasets directly to RADAR,
* `rdmo_radar.imports.RadarImport`, which lets users import RADAR-XML metadata files (exported from RADAR) into RDMO.

The `RadarExportProvider` plugin uses [OAUTH 2.0](https://oauth.net/2/), so that users use
their respective accounts in both systems.


### RDMO Zenodo plugin

https://github.com/rdmorganiser/rdmo-plugins-zenodo

This plugin implements an [export provider](https://rdmo.readthedocs.io/en/latest/plugins/index.html#export-providers)
for RDMO, which lets users push metadata from RDMO to Zenodo work packages. The plugin uses
[OAUTH 2.0](https://oauth.net/2/), so that users use their respective accounts in both systems.
It creates only the metadata in Zenodo, so that users need to upload the actual data on Zenodo themselfes.


### RDMO GitHub plugin

https://github.com/rdmorganiser/rdmo-plugins-github

This repo implements two plugins for [RDMO](https://github.com/rdmorganiser/rdmo):

* an [issue provider](https://rdmo.readthedocs.io/en/latest/plugins/index.html#issue-providers),
  which lets users push their tasks from RDMO to GitHub issues.
* a [project import plugins](https://rdmo.readthedocs.io/en/latest/plugins/index.html#project-import-plugins),
  which can be used to import projects from (public or private)repos.

The plugin uses [OAUTH 2.0](https://oauth.net/2/), so that users use their respective accounts in both systems.


### RDMO GitLab plugin

https://github.com/rdmorganiser/rdmo-plugins-gitlab

This repo implements two plugins for [RDMO](https://github.com/rdmorganiser/rdmo):

* an [issue provider](https://rdmo.readthedocs.io/en/latest/plugins/index.html#issue-providers),
  which lets users push their tasks from RDMO to GitLab issues.
* a [project import plugins](https://rdmo.readthedocs.io/en/latest/plugins/index.html#project-import-plugins),
  which can be used to import projects from (public or private)repos.

The plugin uses [OAUTH 2.0](https://oauth.net/2/), so that users use their respective accounts in both systems.


### RDMO OpenProject plugin

https://github.com/rdmorganiser/rdmo-plugins-openproject

This plugin implements an [issue provider](https://rdmo.readthedocs.io/en/latest/plugins/index.html#issue-providers)
for RDMO, which lets users push their tasks from RDMO to OpenProject work packages. The plugin uses
[OAUTH 2.0](https://oauth.net/2/), so that users use their respective accounts in both systems.


## Plugins contributed by the community

### RDMO Sensor AWI optionset plugin

https://github.com/hafu/rdmo-sensor-awi

Queries the Sensor Information System of the Alfred-Wegener-Institut, Helmholtz-Zentrum für Polar- und Meeresforschung (AWI).

This is an example optionset plugin, to show how to gather information from other systems.
