"""
:Module Name: **log_utils**

============================

This module contains the functions to setup the logging

"""
import logging
import os
import sys
import time

import vc_buildserver.common.log as log_instance
from vc_buildserver.common.platform_utils import get_default_logdirectory
from vc_buildserver.common.platform_utils import get_login


root = logging.root
log = logging.getLogger('vc-tools')

# ---------------------------------------------------
# Setup logging
# ---------------------------------------------------


def _setup_logging():
    """

    This function is for setting up the log

    :return: ``log directory``
    :rtype: ``string``
    """
    logdirectory = _make_log_dir()
    fmt = log_instance.StdFormatter()
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(fmt)
    root.addHandler(stdout_handler)
    root.setLevel(logging.DEBUG)
    lci_logger = log_instance.LogHandler(
        logdirectory, 'vc_buildserver.log',
    )
    lci_logger.setLevel(logging.DEBUG)
    root.addHandler(lci_logger)
    root_logger = log_instance.LogHandler(
        logdirectory, 'vc_buildserver_all.log',
    )
    root_logger.setLevel(logging.DEBUG)
    root.addHandler(root_logger)
    log.info('Logging has been setup')
    return logdirectory


def _make_log_dir():
    """

    This function to create the log directory

    :return:  ``path of the log directory``
    :rtype: ``string``
    """
    logdirectory = os.path.join(
        get_default_logdirectory(), get_login(),
        time.strftime('%Y%m%d-%H%M%S'),
    )
    return _make_unique_log_dir(logdirectory)


def _make_unique_log_dir(desired_logdir, counter_limit=500):
    """

    This function  makes a unique log directory based on the desired_logdir
    path. Append _n(where n<= 500) to the basename as required to
    make sure we don't overwrite an existing directory.

    :param desired_logdir: ``name of the log directory``
    :param counter_limit: ``limit to add to the directory``
                            -*This is to avoid directories with same name*
    :type desired_logdir: ``string``
    :type counter_limit: ``int``
    """
    logdirectory = desired_logdir
    canary_logfile = 'lci_frontend.log'
    for counter in range(0, counter_limit):
        if counter != 0:
            logdirectory = '{}_{:d}'.format(desired_logdir, counter)

        if not os.path.exists(logdirectory):
            os.makedirs(logdirectory)

        logfile = os.path.join(logdirectory, canary_logfile)
        if os.path.exists(logfile):
            # Some other LCI Test has already started using this
            # directory
            continue
        try:
            # Create the file mutually exclusively
            fd = os.open(logfile, os.O_CREAT | os.O_EXCL)
        except OSError:
            # Some other process created the file before we could
            continue
        else:
            # We managed to win the race
            os.close(fd)
            break
    else:
        raise Exception('Unique log directory counter limit exceeded')
    return logdirectory
