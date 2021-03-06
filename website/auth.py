from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Staff, Manager
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cred = request.form.get('cred')

        print(cred, type(cred))

        if cred=="Staff":
            print("yes")
            user = Staff.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    print("there")
                    return redirect(url_for('views.home_staff'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')

        elif cred=="Customer":
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')

        elif cred=="Manager":
            user = Manager.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home_manager'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
        

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        cred = request.form.get('cred')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            return redirect('/sign-up')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
            return redirect('/sign-up')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            return redirect('/sign-up')
        elif len(password1) < 5:
            flash('Password must be at least 5 characters.', category='error')
            return redirect('/sign-up')
        else:
            pass
        
        if cred == "Customer":
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                    password1, method='sha256'), cred = 1)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))

        elif cred=="Staff":
            staff = Staff.query.filter_by(email=email).first()
            if staff:
                flash('Email already exists.', category='error')
            else:
                new_staff = Staff(email=email, first_name=first_name, password=generate_password_hash(
                    password1, method='sha256'), cred = 2)
                db.session.add(new_staff)
                db.session.commit()
                login_user(new_staff, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home_staff'))

        elif cred=="Manager":
            manager = Manager.query.filter_by(email=email).first()
            if manager:
                flash('Email already exists.', category='error')
            else:
                new_manager = Manager(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), cred = 3)
                db.session.add(new_manager)
                db.session.commit()
                login_user(new_manager, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home_manager'))

    return render_template("sign_up.html", user=current_user)
