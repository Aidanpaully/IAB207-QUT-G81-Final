import datetime
from flask import Blueprint, flash, render_template , redirect, request, session, url_for
from flask_login import current_user, login_required
from .forms import EventForm, LoginForm, RegisterForm, ContactForm

main_bp = Blueprint('main', __name__)
from . import db
# Import your models and other necessary dependencies
from .models import Booking, Event, Comment, User  # Import your models here


# for upcoming events
@main_bp.route('/')
def index():
    # Fetch data from your database, including event image data
    events = Event.query.all()  # Replace with your actual query
    # Fetch upcoming events
    upcoming_events = Event.query.filter(Event.date > datetime.date.today()).limit(3).all()  # Adjust the query to fetch upcoming events
    return render_template('index.html', events=events, upcoming_events=upcoming_events)





@main_bp.route('/event_detail', defaults={'event_id': None})
@main_bp.route('/event_detail/<int:event_id>')
def event_detail(event_id):
    if event_id is not None:
        # Fetch the event data from your database using the event_id
        event = Event.query.get(event_id)  # Replace with your actual query

        if event is not None:
            # Fetch comments for the event
            comments = Comment.query.filter_by(event_id=event_id).all()  # Replace with your actual query
            return render_template('event_detail.html', event=event, comments=comments)

    # Handle the case where there is no event ID or the event does not exist
    return render_template('event_detail.html', event=None, comments=None)




@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check if the email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('User with this email already exists. Please log in or use a different email.', 'danger')
        else:
            # Create a new user only if the email is unique
            new_user = User(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,  # You should hash and salt the password
                contact_number=form.contact_number.data,
                address=form.address.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)




@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        # Check username and password
        # If login is successful, set the session variable
        session['logged_in'] = True  # You can set this to the user's ID or any relevant data
        return redirect(url_for('main.index'))

    return render_template('login.html', form=login_form)

@main_bp.route('/logout')
def logout():
    # Clear the user's session to log them out
    session.pop('logged_in', None)
    return redirect(url_for('main.index'))


@main_bp.route('/booking_history')
@login_required  # Use the @login_required decorator to restrict access to logged-in users
def booking_history():
    # Assuming you have a user_id available (e.g., from the currently logged-in user)
    user_id = current_user.id  # Replace with the actual user_id

    # Query booking history for the user
    booking_history = Booking.query.filter_by(user_id=user_id).all()

    return render_template('booking_history.html', booking_history=booking_history)







@main_bp.route('/create_event_update', methods=['GET', 'POST'])
@login_required  # Use the @login_required decorator to restrict access to logged-in users
def create_event():
    form = EventForm()
    
    if form.validate_on_submit():
        # Process the form data and create or update an event
        event = Event(
            title=form.eventName.data,
            description=form.eventDescription.data,
            date=form.eventDate.data,
            status="Open",
            image="default.jpg"
        )
        
        # Associate the event with the current logged-in user
        event.user = current_user
        
        # Save the event to the database
        db.session.add(event)
        db.session.commit()
        
        flash('Event created/updated successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('create_event_update.html', form=form)


# Ensure the user is logged in before booking
@main_bp.route('/book_tickets/<int:event_id>', methods=['POST'])
@login_required
def book_tickets(event_id):
    # Get the quantity of tickets from the form
    ticket_quantity = int(request.form.get('ticketQuantity'))

    # Fetch the event from the database
    event = Event.query.get(event_id)

    # Check if the event is available for booking (add your own checks here)
    if event.status == 'Open':
        # Save the booking to the database
        booking = Booking(user_id=current_user.id, event_id=event.id, quantity=ticket_quantity, booking_date=datetime.now())
        db.session.add(booking)
        db.session.commit()
        flash(f'Success! You have booked {ticket_quantity} ticket(s) for {event.title}.', 'success')
    else:
        flash('Sorry, this event is no longer available for booking.', 'warning')

    return redirect(url_for('main.event_detail', event_id=event.id))



@main_bp.route('/post_comment/<int:event_id>', methods=['POST'])
def post_comment(event_id):
    if request.method == 'POST':
        # Get the user ID from the logged-in user (you should implement user authentication)
        user_id = current_user.id  # You need to adapt this based on your user management
        content = request.form.get('comment_content')
        comment_date = datetime.now()

        # Create a new comment and add it to the database
        comment = Comment(user_id=user_id, event_id=event_id, content=content, comment_date=comment_date)
        db.session.add(comment)
        db.session.commit()

    return redirect(url_for('event_detail', event_id=event_id))