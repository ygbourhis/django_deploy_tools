#!{{ PYTHON_EXEC }}
import os
{% if PROJECT_ROOT %}import sys{% endif %}

{% if ACTIVATE_THIS %}
activate_this = '{{ ACTIVATE_THIS }}'
{% if PY2 %}
execfile(activate_this, dict(__file__=activate_this))
{% elif PY3 %}
exec(
    compile(open(activate_this, "rb").read(), activate_this, 'exec'),
    dict(__file__=activate_this)
)
{% endif %}
{% endif %}
{% if PROJECT_ROOT %}
sys.path.insert(0, '{{ PROJECT_ROOT }}')
{% endif %}
os.environ['DJANGO_SETTINGS_MODULE'] = '{{ DJANGO_SETTINGS_MODULE }}'

from django.core.{{ SGI }} import get_{{ SGI }}_application
application = get_{{ SGI }}_application()
