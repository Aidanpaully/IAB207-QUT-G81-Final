from flask import Blueprint, render_template, redirect, request, url_for, flash
from .forms import LoginForm, RegisterForm

from flask_login import current_user, login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Create a blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Custom decorator to check if the user is authenticated
def login_required_custom(view):
    def wrapped_view(**kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        # Get user input
        user_name = login_form.user_name.data
        password = login_form.password.data

        # Check if the user exists
        user = User.query.filter_by(name=user_name).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html', form=login_form, heading='Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        # Get user input
        user_name = register_form.user_name.data
        email_id = register_form.email_id.data
        password = register_form.password.data

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email_id).first()

        if existing_user:
            flash('Email address already registered. Please log in.')
            return redirect(url_for('auth.login'))

        try:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password, method='sha256')

            # Create a new user with the hashed password
            new_user = User(name=user_name, email=email_id, password=hashed_password)

            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))

        except Exception as e:
            # Handle database errors
            db.session.rollback()
            flash('Registration failed. Please try again later.')
            print(str(e))  # You can log the error for debugging

    return render_template('register.html', form=register_form, heading='Register')

@auth_bp.route('/event_detail', methods=['GET', 'POST'])
@login_required_custom  # Use the custom decorator to require authentication
def create_update_event():
    # Your route code for the Create/Update Event page
    return render_template('event_create_update.html')
