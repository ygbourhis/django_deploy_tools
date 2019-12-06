#!{{ PYTHON_EXEC }}
import os
import sys
{% if ACTIVATE_THIS %}

activate_this = '{{ ACTIVATE_THIS }}'
execfile(activate_this, dict(__file__=activate_this))
{% endif %}
{% if PROJECT_ROOT %}
sys.path.insert(0, '{{ PROJECT_ROOT }}')
{% endif %}
os.environ['DJANGO_SETTINGS_MODULE'] = '{{ DJANGO_SETTINGS_MODULE }}'

from django.core.{{ SGI }} import get_{{ SGI }}_application
application = get_{{ SGI }}_application()
