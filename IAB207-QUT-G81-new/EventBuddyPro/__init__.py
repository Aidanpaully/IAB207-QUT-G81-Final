# Import Flask and necessary extensions
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create an empty SQLAlchemy instance
db = SQLAlchemy()
from .models import Event, Booking, User, Comment

# Create a function that creates a web application
def create_app():
    # Create the Flask app instance
    app = Flask(__name__)  # Use '__name__' to refer to the current module/package

    # Should be set to false in a production environment
    app.debug = True
    app.secret_key = '1234567'

    # Set the app configuration data
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy track modifications
 
    # Initialize db with the Flask app
    db.init_app(app)

    # Initialize the Bootstrap extension with the app
    Bootstrap5(app)

    # Initialize the LoginManager extension
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Set the login view
    login_manager.init_app(app)

    # Import and define the user loader function within the create_app function
    from .models import User
    from . import auth
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import views and auth modules to avoid circular references
    from . import views
    

    # Define the main_bp blueprint
    main_bp = views.main_bp

    # Register the blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth.auth_bp)

    return app
