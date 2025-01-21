# -*- encoding: utf-8 -*-
from flask import render_template, request, jsonify
from flask_login import (
    current_user,
)
from flasgger.utils import swag_from

from apps import db

from apps import login_manager
from apps.authentication.forms import LoginForm
from apps.base import blueprint
import re
import os

from apps.base.models import Company, Product

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
    return True
    # if method in ['POST', 'PATCH', 'DELETE']:
    #     return current_user.is_authenticated
    # if model in ['Company', 'Product']:
    #     return True
    # return current_user.is_authenticated

@blueprint.route('/company/', endpoint='company-without-id', methods=['GET'])
@swag_from('swagger/cmp_without_id_specs.yml', endpoint='base_blueprint.company-without-id', methods=['GET'])
@blueprint.route('/company/<int:cmp_id>', endpoint='company-with-id', methods=['GET'])
@swag_from('swagger/cmp_with_id_specs.yml', endpoint='base_blueprint.company-with-id', methods=['GET'])
@blueprint.route('/company/', endpoint='company-create', methods=['POST'])
@swag_from('swagger/cmp_create_specs.yml', endpoint='base_blueprint.company-create', methods=['POST'])
def company(cmp_id=None):
    if not has_permission('Company', request.method):
        return "You need to be authenticated", 401
    if request.method == 'GET':
        filter_on_fields = {field for field in request.args if hasattr(Company, field)}
        qs = Company.query
        if filter_on_fields:
            # Add filters to query if required
            for field in filter_on_fields:
                expression = (getattr(Company, field) == request.args.get(field))
                qs = qs.filter(expression)
        if cmp_id is not None:
            instance = Company.query.get(cmp_id)
            return jsonify(instance.serialize)
        else:
            return jsonify(data=[i.serialize for i in qs.all()])
    if request.method == 'POST' and request.form:
        name = request.form.get('name')
        cmp_instance = Company(name=name)
        db.session.add(cmp_instance)
        db.session.commit()
        return jsonify(cmp_instance.serialize)


@blueprint.route('/product/', endpoint='product-without-id', methods=['GET'])
@swag_from('swagger/product_without_id_specs.yml', endpoint='base_blueprint.product-without-id', methods=['GET'])
@blueprint.route('/product/<int:product_id>', endpoint='product-with-id', methods=['GET'])
@swag_from('swagger/product_with_id_specs.yml', endpoint='base_blueprint.product-with-id', methods=['GET'])
@blueprint.route('/product/', endpoint='product-create', methods=['POST'])
@swag_from('swagger/product_create_specs.yml', endpoint='base_blueprint.product-create', methods=['POST'])
@blueprint.route('/product/<int:product_id>', endpoint='product-update', methods=['PUT', 'PATCH'])
@swag_from('swagger/product_create_specs.yml', endpoint='base_blueprint.product-update', methods=['PUT', 'PATCH'])
@blueprint.route('/product/<int:product_id>', endpoint='product-delete', methods=['DELETE'])
@swag_from('swagger/product_with_id_specs.yml', endpoint='base_blueprint.product-delete', methods=['DELETE'])
def product(product_id=None):
    if not has_permission('Product', request.method):
        return "You need to be authenticated", 401
    if request.method == 'GET':
        filter_on_fields = {field for field in request.args if hasattr(Product, field)}
        qs = Product.query
        if filter_on_fields:
            # Add filters to query if required
            for field in filter_on_fields:
                expression = (getattr(Product, field) == request.args.get(field))
                qs = qs.filter(expression)
        if product_id is not None:
            instance = Product.query.get(product_id)
            return jsonify(instance.serialize)
        else:
            return jsonify(data=[i.serialize for i in qs.all()])
    if request.method == 'POST' and request.json:
        name = request.json.get('name')
        comment = request.json.get('comment')
        quantity = request.json.get('quantity')
        company_id = request.json.get('company_id')
        product_instance = Product(name=name, comment=comment, quantity=quantity, company_id=company_id)
        db.session.add(product_instance)
        db.session.commit()
        return jsonify(product_instance.serialize)

    if request.method == 'PUT' and request.json:
        product_instance = Product.query.get_or_404(product_id)
        product_instance.name = request.json.get('name') if request.json.get('name') else product_instance.name
        product_instance.comment = request.json.get('comment') if request.json.get('comment') else product_instance.comment
        product_instance.quantity = request.json.get('quantity') if request.json.get('quantity') else product_instance.quantity

        db.session.commit()
        return jsonify(product_instance.serialize)

    if request.method == 'DELETE' and product_id is not None:
        product_instance = Product.query.get(product_id)
        if product_instance is not None:
            db.session.delete(product_instance)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'}), 200
        else:
            return jsonify({'message': 'Product not found'}), 404


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
