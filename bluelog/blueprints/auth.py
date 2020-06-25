# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import render_template, flash, redirect, url_for, Blueprint, current_app, request
from flask_login import login_user, logout_user, login_required, current_user

from bluelog.emails import send_reset_email
from bluelog.forms import LoginForm, Username_PasswordResetRequestForm, Username_PasswordResetForm
from bluelog.models import Admin
from bluelog.utils import redirect_back


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/reset', methods=['GET', 'POST'])
def username_password_reset_request():
    form = Username_PasswordResetRequestForm()
    if form.validate_on_submit():
        admin = Admin.query.first()
        email = form.email.data
        if email in current_app.config['ADMIN_EMAIL']:
            token = admin.generate_reset_token()
            send_reset_email(email, 'Reset Your Username Or Password',
                       'auth/email/reset_username_password',token=token,
                       next=request.args.get('next'))
            flash('An email with instructions to reset your username or password has been '
              'sent to you,Please check your email!')
            return redirect(url_for('auth.login'))
        else:flash('The email you entered is not an administrator email, please re-enter!')
    return render_template('auth/reset_username_password.html', form=form)


@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def username_password_reset(token):
    form = Username_PasswordResetForm()
    admin = Admin.query.first()
    if form.validate_on_submit():
        new_username = form.new_username.data
        new_password = form.new_password.data
        if admin.reset_username_password(token, new_username, new_password):
            flash('Your username or password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    form.new_username.data = admin.username
    return render_template('auth/reset_username_password.html', form=form)










@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
