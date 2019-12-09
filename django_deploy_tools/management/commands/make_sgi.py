import os
import sys
import warnings

import six

from django.core.management import base
from django.template.loader import get_template

from django_deploy_tools import utils


# Suppress Warnings which could clutter the output to the point of
# rendering it unreadable.
warnings.simplefilter('ignore')

cmd_name = utils.get_cmd_name(__name__)

context = {
    'ACTIVATE_THIS': None,
    'DJANGO_SETTINGS_MODULE': utils.DJANGO_SETTINGS_MODULE,
    'PROJECT_ROOT': os.path.dirname(utils.SUPPOSED_PROJECT_PATH),
    'PY2': six.PY2,
    'PY3': six.PY3,
    'PYTHON_EXEC': sys.executable,
}

path_help = "Project path: Insert project path if not on sys.path"

if context['PROJECT_ROOT'] in sys.path:
    path_help += (
        " (detected '%s' already in sys.path so no need to add it, specify "
        "another path if needed)." % context['PROJECT_ROOT']
    )
else:
    path_help += (
        " (detected '%s' which is not in sys.path"
        "use --no-path option if you do not want to "
        "include it)." % context['PROJECT_ROOT']
    )

virtualenv = os.environ.get('VIRTUAL_ENV')
if virtualenv:
    activate_this = os.path.join(
        virtualenv, 'bin/activate_this.py')
    if os.path.exists(activate_this):
        context['ACTIVATE_THIS'] = activate_this


class Command(base.BaseCommand):

    args = ''
    help = """Create a wsgi (default) or asgi file with automatic python
    virtualenv activation.
    """

    def add_arguments(self, parser):
        sgi_group = parser.add_mutually_exclusive_group()

        sgi_group.add_argument(
            "-a", "--asgi",
            default=None, action="store_true",
            help="Output as asgi file (Python 3 only)."
        )
        sgi_group.add_argument(
            "-w", "--wsgi",
            default=None, action="store_true",
            help="Output as wsgi file (default)."
        )

        parser.add_argument(
            "-f", "--force",
            default=False, action="store_true", dest="force",
            help="force overwriting of an existing file"
        )
        parser.add_argument(
            "-o", "--out",
            help="sgi output file."
        )
        parser.add_argument(
            "-p", "--path",
            help=path_help
        )
        parser.add_argument(
            "-n", "--no-path",
            default=False, action="store_true", dest="no_path",
            help="Do not automatically insert %s project path if it's not on "
                 "sys.path (see --path option above), "
                 "I'll handle this myself." % context['PROJECT_ROOT']
        )

    def handle(self, *args, **options):
        force = options.get('force')
        out_file = options.get('out')
        context['SGI'] = 'wsgi'
        for wsgi_type in (
            'asgi', 'wsgi'
        ):
            if options[wsgi_type] is not None:
                context['SGI'] = wsgi_type
        if options.get('path'):
            context['PROJECT_ROOT'] = options['path']
        if context['PROJECT_ROOT'] in sys.path or options['no_path']:
            context['PROJECT_ROOT'] = None
        wsgi_template = get_template('django_deploy_tools/sgi.py')
        rendered_wsgi = wsgi_template.render(context)

        # Generate the WSGI.
        if out_file:
            out_file = os.path.realpath(out_file)
            if not os.path.exists(out_file) or force:
                with open(out_file, 'w') as fp:
                    fp.write(rendered_wsgi)
                print('Generated "%s"' % out_file)  # pylint: disable=C0325
            else:
                sys.exit('"%s" already exists, use --force to overwrite' %
                         out_file)
        else:
            sys.stdout.write(rendered_wsgi)
