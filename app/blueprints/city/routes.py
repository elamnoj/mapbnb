from .import bp as city
from flask import render_template
from flask_login import login_required

@login_required
@city.route('/chicago')
def chi():
    return render_template('cities/chicago.html')

@login_required
@city.route('/austin/')
def austin():
    return render_template('cities/austin.html')

@login_required
@city.route('/boston')
def boston():
    return render_template('cities/boston.html')

@login_required
@city.route('/dallas')
def dallas():
    return render_template('cities/dallas.html')

@login_required
@city.route('/sanfran')
def sanfran():
    return render_template('cities/sanfran.html')
