from logging import StreamHandler
from logging.config import dictConfig

dictConfig(
     {
          "version":1,
          "disable_existing_loggers":False,
          "formatters": {
               "console" : {"format":"[%(name)s:%(lineno)s]%(levelname)s:%(message)s"},
               "file":{
                    "format":"[%(levelname)s] %(asctime)s [%(name)s:%(lineno)s] : %(message)s"
                    }
               },
          
          "handlers": {
               "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "console",
                    "level": "INFO",
               },
               
               "file_filehandler": {
                    "level": "INFO",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter":"file",
                    "when": "midnight",
                    "interval": 1,
                    "backCount": 10,
                    "filename": "./logs/pre-condo.log",
                    "delay":True,              
               },
               
               "updator_filehandler": {
                    "level": "INFO",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter": "file",
                    "when": "midnight",
                    "interval": 1,
                    "backupCount": 10,
                    "filename": "./logs/updator.log",
                    "dealy": True,
                    
               },
          },
          
          "loggers": {
               "": {
                    "level": "INFO",
                    "handlers": ["console", "file_filehandler"],
                    "propagate": False,
               },
               
               "updator": {
                    "level":"DEBUG",
                    "handlers": ["console","updator_filehandler"],
                    "propagate": False,
               },
          },
          
          
     }
     )