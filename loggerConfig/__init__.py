#-*-coding:utf8-*-
from __future__ import absolute_import

import os
import pyhocon

from .logFactory import Handlers, Formatters
from .logFactory import HANDLERS_PATH, FORMATTERS_PATH, LOGGERS_CONF

# Initial default handlers and formatters
PATH = os.path.join(os.path.abspath("."), "base",  "logFactory")
HANDLERS = Handlers(path=os.path.join(PATH, HANDLERS_PATH))
FORMATTERS = Formatters(path=os.path.join(PATH, FORMATTERS_PATH))


def create_logger_conf(handler_type=["file"], formatter_type="dev", log_path=None):
    """Basic Logger"""
    if not log_path is None:
        HANDLERS.sepfileMax = {"path": log_path}
        HANDLERS.file = {"path": log_path}
        HANDLERS.sepfileTime = {"path": log_path}

    # add formatters for each handler
    HANDLERS.console = {"formatter": formatter_type}
    HANDLERS.file = {"formatter": formatter_type}
    HANDLERS.sepfileTime = {"formatter": formatter_type}
    HANDLERS.sepfileTime = {"formatter": formatter_type}

    base = pyhocon.ConfigFactory.parse_file(os.path.join(PATH, LOGGERS_CONF))
    # Add formatters and handlers 
    base.update({"handlers": HANDLERS()})
    base.update({"formatters": FORMATTERS()})

    return base
    


"""
%(levelno)s：打印日志级别的数值。
%(levelname)s：打印日志级别的名称。
%(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]。
%(filename)s：打印当前执行程序名。
%(funcName)s：打印日志的当前函数。
%(lineno)d：打印日志的当前行号。
%(asctime)s：打印日志的时间。
%(thread)d：打印线程ID。
%(threadName)s：打印线程名称。
%(process)d：打印进程ID。
%(processName)s：打印线程名称。
%(module)s：打印模块名称。
%(message)s：打印日志信息。
"""

"""Example
>>> import logging
>>> import logging.config

>>> conf = create_logger_conf(log_path="log.log")
>>> logger_conf = {
        "loggerss": {
            "sample": {
                "handlers": ["console", "file"],
                "level": "INFO"
            }
        }
    }
>>> conf.update(logger_conf)
>>> logging.config.dictConfig(conf)

# now can set logger `sample`
>>> sample = logging.getLogger("sample")
>>> sample.info("This is test message")
"""