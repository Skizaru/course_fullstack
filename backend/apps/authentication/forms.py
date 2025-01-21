# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Pseudo',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Mot de passe',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Pseudo',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe',
                             id='pwd_create',
                             validators=[DataRequired()])

    admin_password = PasswordField('Clé administrateur',
                             id='admin_pwd_create',
                             validators=[DataRequired()])
