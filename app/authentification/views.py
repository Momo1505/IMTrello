from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import authentication
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User, Role, Project


@authentication.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user= login_form_handler(form)

        if user == "error":
            flash('Invalid username or password.')
            return redirect(url_for('.login_page'))
        elif user.role_id == 1:
            return redirect(url_for('main.developer', user_name=current_user.username))
        return redirect(url_for('main.manager', user_name=current_user.username))

    else:

        return render_template('authentication/login.html', form=form)


@authentication.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('.login_page'))


@authentication.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        register_form_handler(form)
        flash('You can now login.')
        return redirect(url_for('authentication.login_page'))
    return render_template('authentication/register.html', form=form)


def login_form_handler(login_form):
    user = User.query.filter_by(email=login_form.email.data).first()
    if user is not None and user.verify_password(login_form.password.data):
        login_user(user, login_form.remember_me.data)
        return user
    else:

        return "error"


def register_form_handler(register_form):
    user = User(name=register_form.name.data,
                email=register_form.email.data,
                username=register_form.username.data,
                password=register_form.password.data,
                role_id=register_form.role.data)
    db.session.add(user)
    db.session.commit()
