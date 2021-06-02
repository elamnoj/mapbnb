from flask import render_template, request, redirect, url_for, flash, current_app as app
from app.blueprints.authentication.models import User
from flask_login import login_user, logout_user
from .import bp as auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is None or user.check_password(request.form.get('password')) is False:
            print('Something is not right')
            flash('User name and email do not match', 'warning')
            return redirect(url_for('auth.login'))
        remember_me = True if request.form.get(
            'checked') is not None else False
        login_user(user, remember=remember_me)
        flash(
            f'Welome, {user.first_name} {user.last_name}! You have successfully logged in!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have logged out successfully.', 'warning')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = User()
        u.from_dict(request.form)
        u.save()
        return redirect(url_for('auth.login'))
    return render_template('register.html')
