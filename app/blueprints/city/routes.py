from .import bp as city
from flask import render_template
from flask_login import login_required

@login_required
@city.route('/chicago')
def chi():
    return render_template('cities/chicago.html')

@login_required
@city.route('/denver/')
def austin():
    return render_template('cities/denver.html')

@login_required
@city.route('/boston')
def boston():
    return render_template('cities/boston.html')

@login_required
@city.route('/la')
def dallas():
    return render_template('cities/la.html')

@login_required
@city.route('/sanfran')
def sanfran():
    return render_template('cities/sanfran.html')
