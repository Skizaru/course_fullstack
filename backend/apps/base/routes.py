# -*- encoding: utf-8 -*-
import sys

from flask import render_template, request, jsonify
from flask_login import (
    current_user,
)
from flasgger.utils import swag_from

from apps import db

from apps import login_manager
from apps.authentication.forms import LoginForm
from apps.base import blueprint
from apps.base.models import *
import re
import os

basedir = os.path.abspath(os.path.dirname(__file__))


@blueprint.route('/')
def route_default():
    login_form = LoginForm(request.form)
    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    return 'API Root - Should return template with actives routes'


def to_pascal_case(s):
    return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), s)


def has_permission(model, method):
    if method in ['POST', 'PATCH', 'DELETE']:
        return current_user.is_authenticated
    if model in ['Customer', 'Product']:
        return True
    return current_user.is_authenticated


@blueprint.route('/company/', endpoint='user-without-id', methods=['GET'])
@swag_from('swagger/cmp_without_id_specs.yml', endpoint='base_blueprint.user-without-id', methods=['GET'])
@blueprint.route('/company/<int:cmp_id>', endpoint='user-with-id', methods=['GET'])
@swag_from('swagger/cmp_with_id_specs.yml', endpoint='base_blueprint.user-with-id', methods=['GET'])
@blueprint.route('/company/', methods=['POST'])
@blueprint.route('/company/<int:cmp_id>', methods=['PATCH'])
@blueprint.route('/company/<int:cmp_id>', methods=['DELETE'])
def company(cmp_id=None):
    pass


@blueprint.route('/<model_name>/', methods=['GET'])
@blueprint.route('/<model_name>/<int:obj_id>', methods=['GET'])
@blueprint.route('/<model_name>/', methods=['POST'])
@blueprint.route('/<model_name>/<int:obj_id>', methods=['PATCH'])
@blueprint.route('/<model_name>/<int:obj_id>', methods=['DELETE'])
def model_api(model_name, obj_id=None):
    model_name = to_pascal_case(model_name)
    form_name = f'{model_name}Form'
    model = getattr(sys.modules[__name__], model_name)
    form_class = getattr(sys.modules[__name__], form_name)

    if not has_permission(model_name, request.method):
        return "You need to be authenticated", 401
    if request.method == 'GET':
        filter_on_fields = {field for field in request.args if hasattr(model, field)}
        qs = model.query
        if filter_on_fields:
            # Add filters to query if required
            for field in filter_on_fields:
                expression = (getattr(model, field) == request.args.get(field))
                qs = qs.filter(expression)

        if obj_id is not None:
            instance = model.query.get(obj_id)
            return jsonify(instance.serialize)
        else:
            return jsonify(data=[i.serialize for i in qs.all()])

    if request.method == 'POST':
        form = form_class(request.form, obj=model)
        if form.validate_on_submit():
            instance = model()
            form.populate_obj(instance)
            db.session.add(instance)
            db.session.commit()
            return jsonify(instance.serialize)

    if request.method == 'PATCH':
        form = form_class(request.form, obj=model)
        if form.validate_on_submit():
            instance = model.query.get_or_404(obj_id)
            form.populate_obj(instance)
            db.session.commit()
            return jsonify(instance.serialize)

    if request.method == 'DELETE' and obj_id is not None:
        instance = model.query.get(obj_id)
        if instance is not None:
            db.session.delete(instance)
            db.session.commit()
            return jsonify({'message': f'{model_name} deleted successfully'}), 200
        else:
            return jsonify({'message': f'{model_name} not found'}), 404


# Errors
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
