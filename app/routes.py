from app import db
from flask import render_template, request, redirect, url_for, flash, current_app as app, jsonify
from app.models import Submit
from app.blueprints.authentication.models import User, StripeCustomer
from flask_login import current_user
import json
import stripe
import os

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "price_id": os.environ["STRIPE_PRICE_ID"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
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
    # customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()

    # # if record exists, add the subscription info to the render_template method
    # if customer:
    #     subscription = stripe.Subscription.retrieve(
    #         customer.stripeSubscriptionId)
    #     product = stripe.Product.retrieve(subscription.plan.product)
    #     context = {
    #         "subscription": subscription,
    #         "product": product,
    #     }
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


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Fulfill the purchase...
        handle_checkout_session(session)

    return "Success", 200


def handle_checkout_session(session):
    s=StripeCustomer()
    s.from_dict(session)
    db.session.add(s)
    db.commit

    # here you should fetch the details from the session and save the relevant information
    # to the database (e.g. associate the user with their subscription)
    print("Subscription was successful.")
