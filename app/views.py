from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, get_or_create
from app.forms import LoginForm
from app.email import send_auth_link


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('stats'))
    form = LoginForm()
    if form.validate_on_submit():
        # creates a user if email is not in db, and returns user if it is
        user = get_or_create(db.session, User, email=form.email.data)
        expiration = 150   # expiration in seconds
        user.generate_auth_link(expiration=expiration)
        send_auth_link(user, expiration=expiration)  # send an email
        flash('The magic link have been sent to {}'.format(form.email.data))
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@login_required
@app.route('/stats')
def stats():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    user = User.query.get(current_user.id)
    return render_template('stats.html', user=user)


@app.route('/auth/<token>', methods=['GET'])
def auth(token):
    user = User.verify_auth_link(token)
    # check not only a correct token but if it's the latest too
    if user and user.auth_link == token:
        login_user(user)
        user.counter += 1
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('stats'))
    elif current_user.is_authenticated:
        return redirect(url_for('stats'))
    else:
        flash('Wrong or expired token. Please, generate new magic link.')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
