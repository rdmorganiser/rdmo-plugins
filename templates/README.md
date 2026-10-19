# RDMO Plugins

This repository contains a list of the currently available [RDMO](https://rdmorganiser.github.io/) plugins.

For additional information, please refer to the corresponding documentation at
https://rdmo.readthedocs.io/en/latest/plugins/index.html.

## Plugins maintained by RDMO

{% for plugin in rdmorganiser -%}
### {{ plugin.title }}

{{ plugin.url }}

{{ plugin.description|trim }}

{% endfor -%}

## Plugins contributed by the community

{% for plugin in shared -%}
### {{ plugin.title }}

{{ plugin.url }}

{{ plugin.description|trim }}

{% endfor -%}
