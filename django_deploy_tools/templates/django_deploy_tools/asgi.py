#!/usr/bin/env python
import os
import sys
{% if ACTIVATE_THIS %}

activate_this = '{{ ACTIVATE_THIS }}'
execfile(activate_this, dict(__file__=activate_this))
{% endif %}
sys.path.insert(0, '{{ PROJECT_ROOT }}')
os.environ['DJANGO_SETTINGS_MODULE'] = '{{ DJANGO_SETTINGS_MODULE }}'

import django.core.asgi
application = django.core.asgi.get_asgi_application()
