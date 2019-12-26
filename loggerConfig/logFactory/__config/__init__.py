#-*-coding:utf8-*-

from __future__ import absolute_import

# import yaml
import logging
import logging.config
import os
import datetime
import abc


CONFIG_PATH = "__config/"

def _create_path(path):
    """Create Directory

    Create log directory which is specified by path.

    Args:
    ------
    path: string, directory path
    """
    if not os.path.exists(path):
        os.mkdir(path)


class Base(metaclass=abc.ABCMeta):
    """Singleton Base MetaClass"""
    _singleton = None
    def __new__(cls, path=None, *args, **kwargs):
        if cls._singleton is None:
            _create_path(path)
            cls._singleton = super().__new__(cls, *args, **kwargs)
        return cls._singleton
    
    def __init__(self, path=None, *args, **kwargs):
        pass

