# -*-coding:utf8-*-
# from __future__ import absolute_import
import os
import sys

import pyhocon

from .__config import Base, CONFIG_PATH


# get config
PATH = os.path.abspath(".")
if not PATH.endswith("logFactory"):
    PATH = os.path.join(PATH, "base/logFactory", CONFIG_PATH)
else:
    PATH = os.path.join(PATH, CONFIG_PATH)

DEFAULT_CONF = CONFIG_PATH + "setup.yaml"

LOGGERS_CONF = os.path.join("__config", "init.conf")
HANDLERS_PATH = os.path.join("__config", "handlers.conf")
FORMATTERS_PATH = os.path.join("__config", "formatters.conf")

__HANDLERS_FILE = os.path.join(PATH, "handlers.conf")
__FORMATTERS_FILE = os.path.join(PATH, "formatters.conf")




class Handlers:
    """Create Handlers Factory
    
    There are several type of handlers that can be used:
    1. console: log information flow to stdout
    2. file: a file saves log information, need add file pathname
    3. sepfileTime: different file saves log information accordding by time.
        Also need a file pathname, besides some arguments is added:
            when: D
            interval: 1
            backupCount: 31
            atTime: datetime.time(11, 59, 59)
    4. sepfileMax: different file saves log information with max storage limitation.
        Also need a file pathname, besides some arguments is added:
            maxBytes: 100 MB
            backupCount: 31

    __handlers_path is the default handlers conf file.
    """

    __handlers_path = os.path.join(PATH, "handlers.conf")

    def __init__(self, path=None):
        """Create Handlers
        
        If handlers path is None, use default handlers path
        """
        if path is None:
            path = self.__handlers_path
        self.handlers = pyhocon.ConfigFactory.parse_file(path)

    @property
    def console(self):
        """console Handler"""
        key = "console"
        handler = self.handlers.console
        return key, handler

    @console.setter
    def console(self, kwargs):
        """Update Hanlder Config
        
        Update console handler with kwargs that is dict
        """
        self.handlers.console.update(kwargs)

    @property
    def file(self):
        """file Handler"""
        if not self.handlers.file.get("filename"):
            raise ValueError("file Handler doesn't contain log file")
        key = "file"
        handler = self.handlers.file
        return key, handler

    @file.setter
    def file(self, kwargs):
        """Setup file Handlers
        
        The path must be setup, which is set filename. kwargs is dict that can
        used in handler
        """
        path = kwargs.get("path")
        if not path and not self.handlers.file.filename:
            raise ValueError("file Handler missing log file, it has to be added")

        if path:
            self.handlers.file["filename"] = path
            kwargs.pop("path")

        # update config
        self.handlers.file.update(kwargs)

    @property
    def sepfileTime(self):
        """sepfileTime Handler"""
        if not self.handlers.sepfileTime.get("filename"):
            raise ValueError("sepfileTime Handler doesn't contain log file")
        key = "file"
        handler = self.handlers.sepfileTime
        return key, handler

    @sepfileTime.setter
    def sepfileTime(self, kwargs):
        """Setup sepfileTime Handlers
        
        The path must be setup, which is set filename. kwargs is dict that can
        used in handler
        """
        path = kwargs.get("path")
        if not path and not self.handlers.sepfileTime.filename:
            raise ValueError("sepfileTime Handler missing log file, it has to be added")

        if path:
            self.handlers.sepfileTime["filename"] = path
            kwargs.pop("path")

        # update config
        self.handlers.sepfileTime.update(kwargs)

    @property
    def sepfileMax(self):
        """sepfileMax Handler"""
        if not self.handlers.sepfileMax.get("filename"):
            raise ValueError("sepfileMax Handler doesn't contain log file")
        key = "file"
        handler = self.handlers.sepfileMax
        return key, handler

    @sepfileMax.setter
    def sepfileMax(self, kwargs):
        """Setup sepfileMax Handlers
        
        The path must be setup, which is set filename. kwargs is dict that can
        used in handler
        """
        path = kwargs.get("path")
        if not path and not self.handlers.sepfileMax.filename:
            raise ValueError("sepfileMax Handler missing log file, it has to be added")

        if path:
            self.handlers.sepfileMax["filename"] = path
            kwargs.pop("path")

        # update config
        self.handlers.sepfileMax.update(kwargs)


    def __call__(self):
        """Return handlers"""
        return self.handlers


class Formatters:
    """Create formatters Factory
    
    There are several type of formatters that can be used:
    1. brief: time-message
    2. simple: time-level-message
    3. dev: time-module-path-funcName-thread-process-message, used to development
    4. prod: time-level-module-path-funcName-message, used to product env

    __formaters_path is the default formatters conf file.
    """

    __formaters_path = os.path.join(PATH, "formatters.conf")

    def __init__(self, path=None):
        """Create Formatters
        
        If path is None, use default formatter path
        """
        if path is None:
            path = self.__formaters_path
        self.formatters = pyhocon.ConfigFactory.parse_file(path)

    
    @property
    def brief(self):
        """Brief Message Formatter

        Just report time and message information. The property get name and formatter
        """
        key = "brief"
        return key, self.formatters.brief

    
    @brief.setter
    def brief(self, kwargs):
        """Update brief Formatter"""
        self.formatters.brief.update(kwargs)

    
    @property
    def simple(self):
        """Simple Message Formatter

        It's general formater, report time-level-message
        """
        key = "simple"
        return key, self.formatters.simple

    
    @simple.setter
    def simple(self, kwargs):
        """Update simple Formater"""
        self.formatters.simple.update(kwargs)


    @property
    def dev(self):
        """Dev Message Formatter

        It's a formatter used to report time-module-path-funcName-thread-process-message,
        and it's used when development
        """
        key = "dev"
        return key, self.formatters.dev


    @dev.setter
    def dev(self, kwargs):
        """Update dev formatter"""
        self.formatters.dev.update(kwargs)


    @property
    def prod(self):
        """Prod Message Formatter

        It's a formatter used to report time-level-module-path-funcName-message,
        and it's used at product development
        """
        key = "prod"
        return key, self.formatters.prod


    @prod.setter
    def prod(self, kwargs):
        """Update prod formatter"""
        self.formatters.prod.update(kwargs)

    def __call__(self):
        return self.formatters

__all__ = ("Handlers", "Formatters", "LOGGERS_CONF", "HANDLERS_PATH", "FORMATTERS_PATH")