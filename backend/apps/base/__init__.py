# -*- encoding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='/api'
)
