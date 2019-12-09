# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import multiprocessing
import os
import socket
import sys
import warnings

from django.conf import settings
from django.core.management import base
from django.template.loader import get_template

from django_deploy_tools import utils
from django_deploy_tools.utils import SUPPOSED_PROJECT_PATH
from django_deploy_tools.utils.apache import (
    APACHE2_VERSION,
    find_apache_log_dir
)

# Suppress DeprecationWarnings which clutter the output to the point of
# rendering it unreadable.
warnings.simplefilter('ignore')

cmd_name = utils.get_cmd_name(__name__)
base_cmd_name = sys.argv[0]

PROJECT_PATH = getattr(settings, 'ROOT_PATH', SUPPOSED_PROJECT_PATH)
PROJECT_ROOT = os.path.dirname(PROJECT_PATH)
PROJECT_NAME = os.path.basename(PROJECT_PATH.split(PROJECT_ROOT)[1])

HOSTNAME = socket.getfqdn()
VHOSTNAME = HOSTNAME.split('.')
VHOSTNAME[0] = PROJECT_NAME
VHOSTNAME = '.'.join(VHOSTNAME)

DOMAINNAME = '%s.%s' % (PROJECT_NAME, HOSTNAME)

ADMIN = 'webmaster@%s' % DOMAINNAME

WSGI_FILE = os.path.join(PROJECT_PATH, 'wsgi.py')

context = {
    'ADMIN': ADMIN,
    'APACHE2_VERSION': APACHE2_VERSION,
    'CACERT': None,
    'DJANGO_SETTINGS_MODULE': utils.DJANGO_SETTINGS_MODULE,
    'DOMAINNAME': DOMAINNAME,
    'HOSTNAME': HOSTNAME,
    'LOGDIR': find_apache_log_dir(),
    'PROCESSES': multiprocessing.cpu_count() + 1,
    'PROJECT_NAME': PROJECT_NAME,
    'PROJECT_PATH': PROJECT_PATH,
    'PROJECT_ROOT': PROJECT_ROOT,
    'SSLCERT': '/etc/pki/tls/certs/ca.crt',
    'SSLKEY': '/etc/pki/tls/private/ca.key',
    'STATIC_PATH': settings.STATIC_ROOT,
    'VHOSTNAME': VHOSTNAME,
    'WSGI_FILE': WSGI_FILE
}


class Command(base.BaseCommand):

    args = ''
    help = """Create the contents of an apache vhost configuration file.

example:

    %(base_cmd_name)s %(cmd_name)s --ssl --mail=%(admin)s \
    --project=%(p_name)s --hostname=%(hostname)s --wsgi %(wsgi_file)s


    """ % {
        'base_cmd_name': base_cmd_name,
        'cmd_name': cmd_name,
        'p_name': context['PROJECT_NAME'],
        'wsgi_file': context['WSGI_FILE'],
        'admin': context['ADMIN'],
        'hostname': context['HOSTNAME'],
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--apache-version",
            dest="apache_version",
            type=float,
            help=("Define the apache "
                  "major (as a floating point number) version "
                  "(default : %s)."
                  % context['APACHE2_VERSION']),
            metavar="APACHE_VERSION"
        )
        parser.add_argument(
            "--cacert",
            dest="cacert",
            help=("Use with the --ssl option to define the path"
                  " to the SSLCACertificateFile"),
            metavar="CACERT"
        )
        parser.add_argument(
            "-f", "--force",
            default=False, action="store_true", dest="force",
            help="force overwriting of an existing output file"
        )
        parser.add_argument(
            "-H", "--hostname",
            dest="hostname",
            help=("Define the server's"
                  " hostname (default : %s)") % context['HOSTNAME'],
            metavar="HOSTNAME"
        )
        parser.add_argument(
            "--logdir",
            dest="logdir",
            help=("Define the path to "
                  "the apache log directory(default : %s)"
                  % context['LOGDIR']),
            metavar="CACERT"
        )
        parser.add_argument(
            "-m", "--mail",
            dest="mail",
            help=("Define the web site"
                  " administrator's email (default : %s)") %
                 context['ADMIN'],
            metavar="MAIL"
        )
        parser.add_argument(
            "-n", "--namedhost",
            default=False, action="store_true", dest="namedhost",
            help=("The apache vhost "
                  "configuration will work only when accessed with "
                  "the proper hostname (see --hostname).")
        )
        parser.add_argument(
            "-o", "--out",
            help="apache configuration output file (default to stdout)."
        )
        parser.add_argument(
            "--processes",
            dest="processes",
            help=("Define the number of "
                  "apache processes (by default the number of cpus +1 which "
                  "is %s on this machine).") % context['PROCESSES'],
            metavar="PROCESSES"
        )
        parser.add_argument(
            "-p", "--project",
            dest="project",
            help=("Define the project "
                  "name (default : %s)") % context['PROJECT_NAME'],
            metavar="PROJECT"
        )
        parser.add_argument(
            "-w", "--wsgi",
            dest="wsgi",
            help="path to the wsgi file",
        )
        parser.add_argument(
            "-s", "--ssl",
            default=False, action="store_true", dest="ssl",
            help=("Use with the --apache option. The apache vhost "
                  "configuration will use an SSL configuration")
        )
        parser.add_argument(
            "--sslcert",
            dest="sslcert",
            help=("Use with the --apache and --ssl option to define "
                  "the path to the SSLCertificateFile (default : %s)"
                  ) % context['SSLCERT'],
            metavar="SSLCERT"
        )
        parser.add_argument(
            "--sslkey",
            dest="sslkey",
            help=("Use with the --apache and --ssl option to define "
                  "the path to the SSLCertificateKeyFile "
                  "(default : %s)") % context['SSLKEY'],
            metavar="SSLKEY"
        )

    def handle(self, *args, **options):
        force = options.get('force')
        out_file = options.get('out')

        context['SSL'] = options.get('ssl')

        if options.get('mail'):
            context['ADMIN'] = options['mail']
        if options.get('cacert'):
            context['CACERT'] = options['cacert']
        if options.get('logdir'):
            context['LOGDIR'] = options['logdir'].rstrip('/')
        if options.get('processes'):
            context['PROCESSES'] = options['processes']
        if options.get('project'):
            context['PROJECT_NAME'] = options['project']
        if options.get('hostname'):
            context['VHOSTNAME'] = options['hostname']
        if options.get('sslcert'):
            context['SSLCERT'] = options['sslcert']
        if options.get('sslkey'):
            context['SSLKEY'] = options['sslkey']
        if options.get('apache_version'):
            context['APACHE2_VERSION'] = options['apache_version']
        if options.get('wsgi'):
            context['WSGI_FILE'] = options['wsgi']

        if options.get('namedhost'):
            context['NAMEDHOST'] = context['VHOSTNAME']
        else:
            context['NAMEDHOST'] = '*'

        # Generate the apache configuration.
        if not os.path.isfile(context['WSGI_FILE']):
            sys.exit(
                '%s is not a valid file, please point to an existing wsgi '
                'file with the --wsgi option, and/or generate one with the '
                '"%s %s" command.' % (
                    context['WSGI_FILE'], base_cmd_name, cmd_name
                )
            )
        wsgi_template = get_template(
            'django_deploy_tools/apache_vhost.conf'
        )
        rendered_conf = wsgi_template.render(context)

        if out_file:
            out_file = os.path.realpath(out_file)
            if not os.path.exists(out_file) or force:
                with open(out_file, 'w') as fp:
                    fp.write(rendered_conf)
                print('Generated "%s"' % out_file)  # pylint: disable=C0325
            else:
                sys.exit('"%s" already exists, use --force to overwrite' %
                         out_file)
        else:
            sys.stdout.write(wsgi_template.render(context))
