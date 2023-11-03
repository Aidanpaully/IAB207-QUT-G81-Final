from flask import Blueprint, render_template, redirect, request, url_for, flash, request
from .forms import LoginForm, RegisterForm
from functools import wraps

from flask_login import current_user, login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db
import sqlite3

# Create a blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Custom decorator to check if the user is authenticated
def login_required_custom(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not current_user.is_authenticated:
            if request.path.startswith('/static/') or request.is_xhr:
                return redirect(url_for('auth.login'))
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

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        # Get user input
        user_name = register_form.user_name.data
        email_id = register_form.email_id.data
        password = register_form.password.data
        contact_number = register_form.contact_number.data
        address = register_form.address.data

        # Connect to the SQLite database
        conn = sqlite3.connect('IAB207-QUT-G81-new/instance/sitedata.db')
        cursor = conn.cursor()

        # Check if the user already exists
        cursor.execute('SELECT * FROM user WHERE email = ?', (email_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email address already registered. Please log in.')
            return redirect(url_for('auth.login'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256')

        # Prepare the SQL statement to insert the new user
        insert_sql = '''
        INSERT INTO user (name, email, password, contact_number, address) 
        VALUES (?, ?, ?, ?, ?)
        '''

        try:
            # Execute the SQL statement
            cursor.execute(insert_sql, (user_name, email_id, hashed_password, contact_number, address))
            conn.commit()

            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError as e:
            conn.rollback()
            flash('Registration failed. Please try again later.')
            print(str(e))
        finally:
            # Close the connection
            conn.close()

    return render_template('register.html', form=register_form, heading='Register')

@auth_bp.route('/event_detail', methods=['GET', 'POST'])
@login_required_custom  # Use the custom decorator to require authentication
def create_update_event():
    # Your route code for the Create/Update Event page
    return render_template('event_create_update.html')
