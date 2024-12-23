import yaml
import logging.config

with open('logging_config.yml', 'r') as file:
    config = yaml.safe_load(file)


logging.config.dictConfig(config)
