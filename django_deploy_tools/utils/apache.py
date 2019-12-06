import os
import re
import subprocess

import six

from django_deploy_tools.utils import DEFAULT_LOG_DIR


# Known apache regular expression to retrieve it's version
APACHE_VERSION_REG = r'Apache/(?P<version>[\d.]*)'
# Known apache commands to retrieve it's version
APACHE2_VERSION_CMDS = (
    (('/usr/sbin/apache2ctl', '-V'), APACHE_VERSION_REG),
    (('/usr/sbin/apache2', '-v'), APACHE_VERSION_REG),
)
# Known apache log directory locations
APACHE_LOG_DIRS = (
    '/var/log/httpd',  # RHEL / Red Hat / CentOS / Fedora Linux
    '/var/log/apache2',  # Debian / Ubuntu Linux
)

# Try to detect apache's version
# We fallback on 2.4.
APACHE2_VERSION = None
for cmd in APACHE2_VERSION_CMDS:
    if os.path.exists(cmd[0][0]):
        try:
            reg = re.compile(cmd[1])
            output = subprocess.check_output(cmd[0], stderr=subprocess.STDOUT)
            if isinstance(output, six.binary_type):
                output = output.decode()
            res = reg.search(output)
            if res:
                APACHE2_VERSION = res.group('version')
                break
        except subprocess.CalledProcessError:
            pass
if APACHE2_VERSION:
    ver_nums = APACHE2_VERSION.split('.')
    if len(ver_nums) >= 2:
        try:
            APACHE2_VERSION = float('.'.join(ver_nums[:2]))
        except ValueError:
            pass


def find_apache_log_dir():
    for log_dir in APACHE_LOG_DIRS:
        if os.path.exists(log_dir) and os.path.isdir(log_dir):
            return log_dir
    return DEFAULT_LOG_DIR


APACHE_LOGDIR = find_apache_log_dir()
