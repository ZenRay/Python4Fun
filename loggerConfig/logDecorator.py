#-*-coding:utf8-*-
"""
Module is used to setup logger
"""

import logging


def logged(class_):
    """Decorator
    
    It's a mixin tool to decorate class. Use the function as decorator, so that
    the class has a logger property

    @logged
    class Player:
        def __init__(self):
            ....
    """
    class_.logger = logging.getLogger(class_.__qualname__)

    return class_