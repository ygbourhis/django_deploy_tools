from importlib import import_module
import os
import re
import socket
import subprocess

import six

DJANGO_SETTINGS_MODULE = os.environ['DJANGO_SETTINGS_MODULE']

# Default log directory
DEFAULT_LOG_DIR = '/var/log'

SUPPOSED_PROJECT_PATH = os.path.realpath(
        os.path.dirname(import_module(DJANGO_SETTINGS_MODULE).__file__)
    )


def get_cmd_name(name=__name__):
    """Get command name from __name__ within a file"""
    return name.split('.')[-1]


def get_default_attr(obj, name, default):
    """Like getattr but return `default` if the attr is None or False.

    By default, getattr(obj, name, default) returns default only if
    attr does not exist, here, we return `default` even if attr evaluates to
    None or False.
    """
    value = getattr(obj, name, default)
    if value:
        return value
    else:
        return default
