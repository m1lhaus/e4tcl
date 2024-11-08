# -*- coding: utf-8 -*-

"""
-   Stream redirector - copies all stderr stream to logger as error messages
-   Custom configuration and setup for logger
    - set logging level
    - set default handler to file
    - set ERROR logs to stderr
    - add DEBUG and INFO logs to stdout (only in DEBUG mode)
"""

import logging
import os
import sys
import datetime

IS_WIN32_EXE = sys.argv[0].endswith(".exe")
APP_ROOT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
LOG_DIR = APP_ROOT_DIR + r"\log"


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects stdout/stderr writes to a logger instance.
    """

    def __init__(self, fdnum, logger, log_level=logging.INFO):
        if fdnum == 0:
            sys.stdout = self
            self.orig_output = sys.__stdout__
        elif fdnum == 1:
            sys.stderr = self
            self.orig_output = sys.__stderr__
        else:
            raise Exception("Given file descriptor num: %s is not supported!" % fdnum)

        self.logger = logger
        self.log_level = log_level

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def __getattr__(self, name):
        return self.orig_output.__getattribute__(name)  # pass all other methods to original fd


class InfoFilter(logging.Filter):
    """
    Logging filter. Filters out ERROR messages and higher.
    """

    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)


def setup_logging(enable):
    if not os.path.isdir(LOG_DIR) and enable:
        os.makedirs(LOG_DIR)

    date = datetime.datetime.now()
    msg_format = "%(module)-10s : %(funcName)-15s %(lineno)-.5d  %(levelname)-8s %(asctime)-20s  %(message)s"
    console_formatter = logging.Formatter(msg_format)

    if enable:
        log_path = os.path.join(LOG_DIR, "dqcl_%s.log" % date.strftime("%Y-%m-%d_%H-%M-%S"))
        logging.basicConfig(level=logging.DEBUG, format=msg_format, filename=log_path)

        logger = logging.getLogger('')  # get root logger

        # redirects all stderr output (exceptions, etc.) to logger ERROR level
        sys.stderr = StreamToLogger(1, logger, logging.ERROR)

        # if not win32gui application, add console handlers
        if not IS_WIN32_EXE:
            # setup logging warning and errors to stderr
            console_err = logging.StreamHandler(stream=sys.__stderr__)  # write to original stderr, not to the logger
            console_err.setLevel(logging.WARNING)
            console_err.setFormatter(console_formatter)
            logger.addHandler(console_err)

            # add console handler with the DEBUG level
            console_std = logging.StreamHandler(stream=sys.__stdout__)
            console_std.setLevel(logging.DEBUG)
            console_std.addFilter(InfoFilter())
            console_std.setFormatter(console_formatter)
            logger.addHandler(console_std)

    else:
        logger = logging.getLogger('')  # get root logger
        logger.propagate = False  # disable logging
