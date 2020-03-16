"""
:Module Name: **platform_utils**

==================================

This module contains all the common test functionality which are used
multiple times through out the LCI frame work. Different modules will import
this module and use the functions whichever are required.

"""
import logging
import os
import subprocess
import sys

#from vc.common.watch_dog import Watchdog
#from vc.common.config_data import LciCommon as videocommon

log = logging.getLogger(__name__)


def get_login():
    """

    Platform independent method for retrieving the login name of the current
    user.

    :return: ``logged in username``
    :rtype: ``string``

    """
    if get_platform().startswith('win'):
        return os.environ.get('USERNAME', 'Unknown')
    else:
        return os.environ.get('USER', 'Unknown')


def get_platform():
    """

    This method gets the name of platform ( operating system)

    :return: ``name of the operating system``
    :rtype: ``string``
    """
    return sys.platform


def get_custom_platform():
    """
    This method gets the custom name of platform ( operating system)
    :return: ``name of the operating system``
    :rtype: ``string``
    """
    _platform = sys.platform
    if _platform.startswith('linux'):
        platform = 'linux'
    elif _platform.startswith('darwin'):
        platform = 'macos'
    else:
        platform = 'windows'

    return platform


def get_default_logdirectory():
    """
    This method retrieves the default log directory.

    :return: ``log directory``
    :rtype: ``string``
    """
    try:
        return os.path.join(os.getcwd(), 'vc-buildserver-logs')
    except IOError as io_error:
        raise io_error
