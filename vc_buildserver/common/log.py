"""
:Module Name: **log**

=======================

This module contains the classes for log handling

"""
import logging
import os
import time


class LogHandler(logging.FileHandler):
    """
    LogHandler class is for handling logs generation and log file path
    generation

    """

    def __init__(self, logdirectory, filename, level=logging.DEBUG):
        """
        This is method to initialize the the LogHandler

        :param logdirectory: ``name of the log directory``
        :param filename: ``name of the file``
        :param level: ``log level to be set``
        :type logdirectory: ``string``
        :type filename: ``string``
        :type level: ``string``
        """
        logdirectory = os.path.abspath(logdirectory)
        if not os.path.exists(logdirectory):
            os.makedirs(logdirectory)
        filename = self.generate_filepath(logdirectory, filename)
        logging.FileHandler.__init__(self, filename)
        self.setLevel(level)
        self.setFormatter(FileFormat())

    @classmethod
    def generate_filepath(cls, logdirectory, filename='vc-tools_output.log'):
        """
        This method is for log file path generation

        :param logdirectory : name of the log directory
        :param filename     : name of the file
        :type logdirectory: ``string``
        :type filename: ``string``
        :return: ``log file path name``
        :rtype: ``string``
        """
        return os.path.join(logdirectory, filename)


class StdFormatter(logging.Formatter):
    """

    StringFormatter class to set the format of the logs captured

    """
    std_format = '%(asctime)s:[%(name)s] %(levelname)s %(message)s'

    def __init__(self):
        """
         This is method to initialize the the StdFormatter class

        """
        logging.Formatter.__init__(self, self.std_format)


class ColorFormatter(StdFormatter):
    """
    ColorFormatter class is for setting the colour for log level

    """
    std_format = (
        '%(bold_cyan)s[%(name)s]%(normal)s %(level_color)s'
        '%(levelname)s%(normal)s %(message)s'
    )

    def __init__(self, terminal):
        """

    This is method to initialize the colour for log level

    :param terminal: ``terminal value``
    :type terminal: ``string``
    :return: None
        """
        self.colors = {
            'DEBUG': terminal.magenta,
            'INFO': terminal.green,
            'WARNING': terminal.red,
            'ERROR': terminal.white_on_red,
            'CRITICAL': terminal.bold_white_on_red,
        }
        self.bold_cyan = terminal.bold_cyan
        self.normal = terminal.normal
        StdFormatter.__init__(self)

    def format(self, record):
        """
        This method is to set the colour for record

        :param record: ``record``
        :type record: ``string``
        :return: ``None``
        """
        record.level_color = self.colors.get(record.levelname)
        record.bold_cyan = self.bold_cyan
        record.normal = self.normal
        return logging.Formatter.format(self, record)


class FileFormat(StdFormatter):
    """

    FileFormat class to set the format of the log file

    """
    std_format = '%(asctime)s: [%(name)s] {%(levelname)s} %(message)s'

    def formatTime(self, record, datefmt=None):
        """

       This method is to set the format of the date and time
       :param record: ``record``
       :param datefmt: ``format of date and time``
       :type record: ``string``
       :type datefmt: ``string``
       :return: ``format of the date and time``
       :rtype: ``string``
       """
        if datefmt:
            format_time = StdFormatter.formatTime(self, record, datefmt)
        else:
            time_struct = self.converter(record.created)
            # msecs isn't available in time_struct so inject them manually
            format_time = time.strftime(
                '%Y-%m-%d %H:%M:%S.{:03.0f}  '
                '%Z'.format(record.msecs), time_struct,
            )
        return format_time
