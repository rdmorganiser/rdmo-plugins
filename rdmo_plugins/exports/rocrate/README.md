# ROcrate Export Plugin
This is an export plugin for [RDMO](https://github.com/rdmorganiser/rdmo), it aims to export RDMO projects in the [RO-Crate](https://researchobject.github.io/ro-crate/) format. The user can select which datasets of the RDMO project are included in the RO-Crate export.  

The RDMO attributes are mapped to the RO-Crate metadata properties in the `default.toml` config file. The RO-Crate files are constructed with the help of the [ro-crate-py](https://github.com/ResearchObject/ro-crate-py.git) library. 
The export function creates a zip file containing the `ro-crate-metadata.json`, a JSON-LD file, and empty folders for each selected dataset.

For development purposes there is a web preview setting available, whic can be configure with `ROCRATE_EXPORT_WEB_PREVIEW` in the settings of the `rdmo-app`.
