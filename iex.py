"""
Hacky IEX forward proxy stuff
"""
import configparser
import datetime
import logging
import re
import requests
import urllib.parse

from flask import current_app, request

import request_config


def do_iex(path, args):
    """Proxy the raw incoming request to IEX Cloud.

       @param path: url path
       @param args: query parameters as a dict

       Returns a valid JSON response or raises
    """
    # Parse freshness
    request_config = get_request_config(path, args)
    current_app.logger.debug('Request config: %s', repr(request_config))

    # TODO: If freshness is not None, go to Firestore

    # Build parts of request url
    url_parts = (
        'https',                        # Scheme
        current_app.config['IEX_HOSTNAME'],     # Network location
        path,                           # Path
        '',                             # Params
        'token={}'.format(              # Query args
            current_app.config['IEX_API_KEY']),
        ''                              # Fragment id
    )

    # Build url
    url = urllib.parse.urlunparse(url_parts)
    print(url)

    # Make the request
    current_app.logger.debug('Making request to IEX Cloud service: %s', url)
    r = requests.get(url)
    current_app.logger.debug('Response status_code: %d', r.status_code)

    # Raise for 4xx or 5xx
    r.raise_for_status()

    # Return json response
    return r.json()


def firestore_get():
    """"""


def get_default_config(path):
    """Fetch default configuration dict for the IEX request"""
    # Pattern for replacing stock symbol with generic SYMBOL
    SYMBOL_PATTERN = r'stock/\w+'
    SYMBOL_REPLACE = 'stock/SYMBOL'

    # Pull config parser
    default_config = configparser.ConfigParser()
    default_config.read_dict(request_config.config)

    # Replace symbol in path
    key = re.sub(SYMBOL_PATTERN, SYMBOL_REPLACE, path)
    current_app.logger.debug('Fetching default config for "%s". Using key: "%s"', path, key)

    # If section is not found, use default section
    if not default_config.has_section(key):
        result = default_config['DEFAULT']
    else:
        result = default_config[key]

    # Return dict instead of configparser section
    return {x: y for x, y in result.items()}


def parse_freshness(value):
    """Parse given freshness value and return a timedelta object
       Format should be [INT][s|m|h|d|w] (seconds, minutes, hours, days, weeks).
       If the input is an integer only, we assume days. For example:
        - 120s = 120 seconds
        - 420m = 420 minutes
        - 60d  = 60 days
        - 7    = 7 days

       Returns a datetime.timedelta object representing freshness value.
       Returns None if the input value could not be parsed.
    """
    FRESH_PATTERN = r'^(\d+)([smhdw])$'

    if not isinstance(value, str):
        return None

    match = re.match(FRESH_PATTERN, value)

    if match is None:
        return None

    elif match.group(2) == 's':
        delta = datetime.timedelta(seconds=int(match.group(1)))

    elif match.group(2) == 'm':
        delta = datetime.timedelta(minutes=int(match.group(1)))

    elif match.group(2) == 'h':
        delta = datetime.timedelta(hours=int(match.group(1)))

    elif match.group(2) == 'd':
        delta = datetime.timedelta(days=int(match.group(1)))

    elif match.group(2) == 'w':
        delta = datetime.timedelta(weeks=int(match.group(1)))

    return delta


def get_request_config(path, args):
    """Process query args. Sanity check the given query string args.
       If values are missing or invalid, return a default set of key/values
    """
    # Get default config
    config = get_default_config(path)
    current_app.logger.debug('Default config: "%s"', repr(config))

    # Parse raw freshness
    freshness = parse_freshness(args.get('freshness', None))
    current_app.logger.debug('Parsed freshness: "%s"', repr(freshness))

    # If valid freshness is given, overwrite the default
    if freshness is not None:
        config['freshness'] = freshness

    return config
