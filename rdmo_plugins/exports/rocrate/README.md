# ROcrate Export Plugin
This is an export plugin for [RDMO](https://github.com/rdmorganiser/rdmo), that was created during the [RDMO Hackathon 2023](https://www.forschungsdaten.org/index.php/RDMO_Hackathon_2023)

It aims to export RDMO projects in the [RO-Crate](https://researchobject.github.io/ro-crate/) format. The user can select which datasets of the RDMO project are included in the RO-Crate export.  

The RDMO attributes are mapped to the RO-Crate metadata properties in the `rdmo-rocrate.toml` config file. The RO-Crate files are constructed with the help of the [ro-crate-py](https://zenodo.org/record/8005944) library.
The export function creates a zip file containing the `ro-crate-metadata.json`, a JSON-LD file, filled the with metadata values that were extracted from the RDMO project. Individual datasets can be selected to be included in the export, when the project contains datasets. The metadata of each dataset is added to the `ro-crate-metadata.json` file and empty folders are created for each dataset (for the directory tree).

## Setup

Install the plugin in your RDMO virtual environment using pip (directly from GitHub):
```bash
pip install git+https://github.com/rdmorganiser/rdmo-plugins-rocrate.git
```
The dependencies [`ro-crate-py`](https://pypi.org/project/rocrate/) and [`tomli`](https://pypi.org/project/tomli/) will be installed automatically.
Add the `rdmo_plugins_rocrate` app to your `INSTALLED_APPS` in `config/settings/local.py``:
```py
from . import INSTALLED_APPS
INSTALLED_APPS = ['rdmo_plugins_rocrate'] + INSTALLED_APPS
```

As default the export will be as a zip file download.
For development purposes there is a web preview setting available. This feature can be configured by a boolean setting in the `rdmo-app` with the name `ROCRATE_EXPORT_WEB_PREVIEW`, it can be omitted and will default to False.
```py
'''
A boolean setting to enable the web preview feature of the rocrate export plugin.
Default: False
Purpose: Local development
'''
ROCRATE_EXPORT_WEB_PREVIEW = True # default is False and this setting can be omitted
```
