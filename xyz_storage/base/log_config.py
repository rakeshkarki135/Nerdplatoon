import os
from logging import StreamHandler
from logging.config import dictConfig

if not os.path.exists("./logs/"):
    os.makedirs("./logs/")


dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {"format":"[%(name)s:%(lineno)s] %(levelname)s : %(message)s"},
            "file" : {"format":"[%(levelname)s %(asctime)s] [%(name)s:%(lineno)s] : %(message)s"},      

        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
                "level": "INFO",
            },

            "file_filehandlers": {
                "level" :"INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "file",
                "when": "midnight",
                "interval": 1,
                "backupCount": 10,
                "filename": "./logs/xyz_storage.log",
                "delay": True,
            },

            "xyz_storage_filehandlers" :{
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "file",
                "when": "midnight",
                "interval": 1,
                "backupCount" : 10,
                "filename": "./logs/xyz_storage.log",
                "delay": True,

            },
        },

        "loggers" : {
            "": {
                "level": "INFO",
                "handlers": ["console", "file_filehandlers"],
                "propagate": False,
            },
            "xyz_storage": {
                "level": "INFO",
                "handlers" : ["console", "xyz_storage_filehandlers"],
                "propagate": False,
            },
        },


    }
)
