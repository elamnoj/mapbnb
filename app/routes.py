from app import db
from flask import render_template, request, redirect, url_for, flash, current_app as app, jsonify
from app.models import Submit
from app.blueprints.authentication.models import User
from flask_login import current_user
import json
import stripe
import os

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "price_id": os.environ["STRIPE_PRICE_ID"],  # new
}


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        if user is not None:
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')

            if request.form.get('password') and request.form.get('confirm_password') and request.form.get('password') == request.form.get('confirm_password'):
                user.password = request.form.get('password')
            elif not request.form.get('password') and not request.form.get('confirm_password'):
                pass
            else:
                flash(
                    'There was an issue updating your information. Please try again.', 'warning')
                return redirect(url_for('profile'))
            db.session.commit()
            flash('User updated successfully', 'success')
            return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        s = Submit()
        s.from_dict(request.form)
        db.session.add(s)
        db.session.commit()
        flash('Thank you for your submission!')
        return redirect(url_for('home'))
    return render_template('contact.html')


@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://localhost:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        checkout_session = stripe.checkout.Session.create(
            # client_reference_id=user.id,
            success_url=domain_url + \
            "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancel",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": stripe_keys["price_id"],
                    "quantity": 1,
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/success")
def success():
    return render_template("register.html")


@app.route("/cancel")
def cancelled():
    return render_template("cancel.html")
