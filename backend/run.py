# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from sys import exit

from flask_cors import CORS

from apps.config import config_dict
from apps import create_app
from flasgger import Swagger
from flask import request

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"], headers=["Content-Type", "Authorization"])

Swagger(app)



@app.before_request
def handle_options_request():
    if request.method == 'OPTIONS':
        response = app.response_class(status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response


if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG))
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE')
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
