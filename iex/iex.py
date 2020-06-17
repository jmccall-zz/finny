"""
Hacky IEX forward proxy stuff
"""
import configparser
import re

import request_config

def parse_freshness(value):
    """Parse given freshness value and return a timedelta object
       Format should be [INT][s|m|d]. If the input is an integer only,
       we assume days. For example:
        - 120s = 120 seconds
        - 420m = 420 minutes
        - 60d  = 60 days
        - 7    = 7 days

       Returns a datetime.timedelta object representing freshness value.
       Returns None if the input value could not be parsed.
    """

def get_default_config(path):
    """Fetch default configuration dict for the IEX request"""
    default_config = configparser.ConfigParser()
    default_config.read_dict(request_config.config)
