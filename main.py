# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
# import logging
import os
import requests
import urllib.parse

from flask import Flask, url_for, send_from_directory
import dividends


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask('finny')

# Init app.logger which adds default handlers
# for handler in app.logger.handlers:
#     logging.root.addHandler(handler)

# app.logger.debug('Finny server starting ...')

# Load app configuration
app.config.from_pyfile('settings.cfg')

# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Say hello at root
@app.route('/')
def hello():
    """Say hello!"""
    return "tranquiloooo"

@app.route('/iex/', defaults={'path': 'path'})
@app.route('/iex/<path:path>', methods=['GET', 'POST'])
def iex(path):
    """Reverse proxy for IEX Cloud API"""
    # Build parts of request url
    url_parts = (
        'https',                        # Scheme
        app.config['IEX_HOSTNAME'],     # Network location
        path,                           # Path
        '',                             # Params
        'token={}'.format(              # Query args
            app.config['IEX_API_KEY']),
        ''                              # Fragment id
    )

    # Build url
    url = urllib.parse.urlunparse(url_parts)
    print(url)

    # Make the request
    app.logger.debug('Making request to IEX Cloud service: %s', url)
    r = requests.get(url)
    app.logger.debug('Response status_code: %d', r.status_code)

    # Raise for 4xx or 5xx
    r.raise_for_status()

    # Return json response
    return r.json()


@app.route('/div/<symbol>')
def yeet(symbol):
    """Do the stuffzz"""
    app.logger.debug('do yeet')
    # import pdb; pdb.set_trace()
    r = dividends.get_div_years_of_growth(symbol)

    # import pdb; pdb.set_trace()
    # app.logger.debug('Done with yeet')

    return symbol


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
