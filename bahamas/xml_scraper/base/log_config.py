import os 
from logging.config import dictConfig
from logging import StreamHandler

if not os.path.exists("./logs/"):
    os.makedirs("./logs/")



dictConfig(
    {
        "version":1,
        "disable_existing_loggers":False,
        "formatters": {
            "console":{"format":"[%(name)s:%(lineno)s] %(levelname)s : %(message)s"},
            "file":{"format":"[%(levelname)s:%(asctime)s] [%(name)s:%(lineno)s] : %(message)s"}
        },
        
        "handlers" : {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
                "level": "INFO",
                
            },
            
            "file_filehandlers":{
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "file",
                "when": "midnight",
                "interval": 1,
                "backupCount" : 10,
                "filename": "./logs/xml_extractor.log",
                "delay": True
            },
            
            "links_filehandlers":{
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "file",
                "when": "midnight",
                "interval": 1,
                "backupCount": 10,
                "filename": "./logs/xml_links.log",
                "delay": True 
            },
            "merger_filehandlers":{
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "file",
                "when": "midnight",
                "interval": 1,
                "backupCount": 10,
                "filename": "./logs/xml_merger.log",
                "delay": True 
            }
        },
        
        "loggers" : {
            "": {
                "level": "INFO",
                "handlers": ["console","file_filehandlers"],
                "propagate": False,
            },
            
            "links":{
                "level":"INFO",
                "handlers":["console", "links_filehandlers"],
                "propagate":False
            },
            "merger": {
                "level": "INFO",
                "handlers": ["console","merger_filehandlers"],
                "propagate":False,
            }
        }
    }
    
)