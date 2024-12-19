import os
from logging import StreamHandler
from logging.config import dictConfig

# Create the logs directory if it doesn't exist
if not os.path.exists('./logs/'):
    os.mkdir('./logs/')

# Configure logging
dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(name)s:%(lineno)s] %(levelname)s : %(message)s"
        },
        "file": {
            "format": "[%(levelname)s %(asctime)s] [%(name)s:%(lineno)s] : %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "level": "INFO",
        },
        "file_handler": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file",
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
            "filename": "./logs/mesora.log",
            "delay": True,
        },
        "link_file_handler": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file",
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
            "filename": "./logs/links.log",
            "delay": True,
        },
        "detail_file_handler": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file",
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
            "filename": "./logs/details.log",
            "delay": True,
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console", "file_handler"],
            "propagate": False,
        },
        "link_logger": {
            "level": "INFO",
            "handlers": ["console", "link_file_handler"],
            "propagate": False,
        },
        "details": {
            "level": "INFO",
            "handlers": ["console", "detail_file_handler"],
            "propagate": False,
        },
    }
})
