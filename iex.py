"""
Hacky IEX forward proxy stuff
"""
import configparser
import datetime
import json
import logging
import re
import requests
import request_config
import urllib.parse

from google.cloud import firestore

from flask import Blueprint, current_app, request

bp = Blueprint('auth', __name__, url_prefix='/iex')

@bp.route('/<version>/stock/<symbol>/<path:method>', methods=('GET',))
def stock(version, symbol, method):
    """IEX stable stock endpoint for quotes, company info, etc."""
    ENDPOINT = 'stock'
    # Trim trailing slashes from method
    method = method.rstrip('/')
    current_app.logger.info('IEX request received: "%s\n - Version: %s\n - Symbol: %s\n - Method: %s"',
            request.full_path, version, symbol, method)

    # Get request config for api call
    config = get_request_config(ENDPOINT, method, request.args)
    current_app.logger.info('Compiled request config: %s', repr(config))

    # Get a document id for the given request path
    id = path_to_document_id(request.path)

    # Get document from firestore
    doc = get_firestore_doc(id)
    current_app.logger.debug('Firestore document fetch done.')

    # If record is found check it's age
    if doc.exists:
        # Get age of document
        age = datetime.datetime.utcnow() - doc.update_time.ToDatetime()
        current_app.logger.debug('Document exists:\n - Data: %s\n - Update time: %s\n - Age: %s',
                repr(doc.to_dict()),
                doc.update_time.ToDatetime(),
                age)

        # If record is fresh just return it
        if age < config['freshness']:
            return prep_response(doc.to_dict())

    # Strip leading "/iex" that we don't want to send with the request
    path = request.path.lstrip(bp.url_prefix)

    # Proxy to IEX cloud for data. Exception is raised if call fails
    data = hit_iex(path)
    current_app.logger.debug('IEX proxy done: %s', data)

    # Write record to firestore
    try:
        current_app.logger.debug('Writing data to firestore: (%s, %s)', id, data)
        set_firestore_doc(id, data)
    except Exception as e:
        current_app.logger.error('Failed to create new document:\n - Id: %s\n - Data: %s\n - Error: %s',
                id,
                data,
                e.message)

    return prep_response(data)

# ---

def get_default_config(endpoint, method):
    """Fetch default configuration dict for the IEX request"""
    DEFAULT_ENDPOINT = 'stock'

    # Get input config dict using endpoint
    if endpoint in request_config.config:
        input_dict = request_config.config[endpoint]
    else:
        input_dict = request_config.config[DEFAULT_ENDPOINT]

    current_app.logger.debug('Input dict: %s', repr(input_dict))

    # Generate config parser
    default_config = configparser.ConfigParser()
    default_config.read_dict(input_dict)

    # Replace symbol in path
    current_app.logger.debug('Fetching default config for (%s, %s)', endpoint, method)

    # If section is not found, use default section
    if not default_config.has_section(method):
        result = default_config['DEFAULT']
    else:
        result = default_config[method]

    # Return dict instead of configparser section
    return {x: y for x, y in result.items()}

def get_request_config(endpoint, method, args):
    """Process query args. Sanity check the given query string args.
       If values are missing or invalid, return a default set of key/values.
    """
    # Get default config
    config = get_default_config(endpoint, method)

    # Freshness string to timedelta
    config['freshness'] = parse_freshness(config['freshness'])
    current_app.logger.debug('Default request config: "%s"', repr(config))

    # Parse raw freshness. Returns a timedelta freshness or None
    freshness = parse_freshness(args.get('freshness', None))
    current_app.logger.debug('Parsed freshness: "%s"', repr(freshness))

    # If valid freshness is given, overwrite the default
    if freshness is not None:
        config['freshness'] = freshness
        current_app.logger.debug('Overwriting freshness config: "%s"', repr(freshness))

    return config


def get_firestore_doc(id):
    """Fetch a record from firestore"""

    # Init db
    current_app.logger.debug('Init firestore client: %s', current_app.config['FIRESTORE_PROJECT'])
    db = firestore.Client(current_app.config['FIRESTORE_PROJECT'])

    # Init document ref
    doc_ref = db.collection(current_app.config['FIRESTORE_IEX_COLLECTION']).document(id)

    current_app.logger.debug('Fetching document: (%s, %s)',
            current_app.config['FIRESTORE_IEX_COLLECTION'],
            id)

    doc = doc_ref.get()

    return doc

def hit_iex(path):
    """Make a request to Cloud IEX given path"""
    # IEX only allows certain query string ags
    ALLOWED_ARGS = [
        'range',
        'symbol',
        'symbols',
        'token',
    ]
    args = {x: y for x, y in request.args.items() if x in ALLOWED_ARGS}

    # Build parts of request url
    url_parts = (
        'https',                              # Scheme
        current_app.config['IEX_HOSTNAME'],   # Network location
        path,                                 # Path
        '',                                   # Params
        urllib.parse.urlencode(args),         # Query args
        ''                                    # Fragment id
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
    FRESH_PATTERN = r'^(\d+)([smhdw])?$'

    if not isinstance(value, str):
        return None

    match = re.match(FRESH_PATTERN, value)

    if match is None:
        return None

    # If a time symbol wasn't given, use days
    elif match.group(2) is None:
        delta = datetime.timedelta(days=int(match.group(1)))

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

def path_to_document_id(path):
    """Return firestore collection document_id given request path"""
    return path.replace('/', '')

def prep_response(data):
    """Given a document dict, prep it to be returned to user"""
    # Get JSONEncoder
    encoder = json.JSONEncoder()
    # Convert to string if data is single int or float
    if isinstance(data, int) or isinstance(data, float):
        return encoder.encode(str(data))

    # Extra checks for dict type data
    elif isinstance(data, dict):
        # If dict has a single key and it's "value" we assume that this
        # is a record from firestore. In the case we receive single values
        # from IEX, we use a default key for use in the document. When we
        # return back to end users we only return the value, just like they'd
        # expect if hitting IEX directly
        if len(data.keys()) == 1 and current_app.config['FIRESTORE_VALUE_KEY'] in data:
            return encoder.encode(str(data[current_app.config['FIRESTORE_VALUE_KEY']]))

    return encoder.encode(data)

def set_firestore_doc(id, data):
    """Create firestore document"""
    current_app.logger.debug('Init firestore client: %s', current_app.config['FIRESTORE_PROJECT'])
    db = firestore.Client(current_app.config['FIRESTORE_PROJECT'])

    # Init document ref
    doc_ref = db.collection(current_app.config['FIRESTORE_IEX_COLLECTION']).document(id)

    # If data isn't a dictionary, make it one
    if isinstance(data, str):
        data = {current_app.config['FIRESTORE_VALUE_KEY']: data}
    elif isinstance(data, int) or isinstance(data, float):
        data = {current_app.config['FIRESTORE_VALUE_KEY']: str(data)}

    # Create or update document
    doc_ref.set(data)
