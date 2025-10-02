# Imports
from project import db, app
from project.decorators import permission_required
from flask import render_template, redirect, request, url_for, flash 
from flask_login import login_user, login_required, logout_user
from project.models import User
from project.forms import RegistrationForm, LoginForm 
from distutils.log import debug
from fileinput import filename

# Create the first admin user if not already present
with app.app_context():
    admin = User.query.filter_by(email="admin@example.com").first()
    if not admin:
        admin = User(
            name="Admin User",
            email="admin@example.com",
            password="admin123",   # password hashed in User model
            role="board"
        )
        print(admin.role)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@example.com / admin123")

# Route to upgrade a user's role (board only)
@app.route("/upgrade/user", methods=["POST"])
@login_required
@permission_required('board')
def upgrade_user():
    user_id = request.form.get("user_id", type=int)  # Get user ID from form
    role_choice = request.form.get("role_choice", type=str)  # Get new role

    if not user_id:
        flash("No user selected.")
        return redirect(url_for("board_dashboard"))
    
    user = User.query.get(user_id)  # Find user by ID

    if user is None:
        flash("User not found!")
        return redirect(url_for("board_dashboard"))
    
    user.role = role_choice  # Update user role
    db.session.commit()
    flash(f"User {user.name} has been upgraded to {user.role} .")
    return redirect(url_for("board_dashboard"))
    
# Home page for general users
@app.route("/")
def user_dashboard():
    return render_template("user_home.html")

# Dashboard for interns (intern only)
@app.route("/intern/dashboard")
@login_required
@permission_required('intern')
def intern_dashboard():
    return render_template("intern_home.html")

# Dashboard for volunteers (volunteer only)
@app.route("/volunteer/dashboard")
@login_required
@permission_required('volunteer')
def volunteer_dashboard():
    return render_template("volunteer_home.html")

# Dashboard for board members (board only)
@app.route("/board/dashboard")
@login_required
@permission_required('board')
def board_dashboard():
    user = User.query.all()  # Get all users
    return render_template("board_home.html", user = user)

# File upload success handler
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  # Get uploaded file
        f.save(f.filename)         # Save file to disk
        return render_template("acknowledgement.html", name = f.filename)  
    
# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()  # Create registration form
    
    if request.method == "POST":
        if form.validate_on_submit():  # If form is valid
            user = User(
                name=form.data['name'], 
                email=form.data['email'], 
                password=form.data['password']
            )
            db.session.add(user)
            db.session.commit()
            flash("You have successfully registered!")
            return redirect(url_for("login"))
        else:
            flash("Error")
            print("Form errors:", form.errors)

    return render_template('register.html', form=form) 

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create login form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Find user by email

        if user is not None and user.check_password(form.password.data):
            login_user(user)  # Log in user
            flash('Logged in successfully.')

            # Redirect user based on their role
            print(user.role)
            if user.role == "board":
                return redirect(url_for("board_dashboard"))
            elif user.role == "intern": 
                return redirect(url_for("intern_dashboard"))
            elif user.role == "volunteer": 
                return redirect(url_for("volunteer_dashboard"))
            else:   
                return redirect(url_for("user_dashboard"))
        else:
            if user is None:
                flash('Email does not exist.')
            else: 
                flash('Invalid email or password.')

    return render_template('login.html', form=form)

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()  # Log out user
    flash("You have successfully logged out!")
    return redirect(url_for("user_dashboard"))

# Run the app if this file is executed directly
if __name__ == "__main__": 
    app.run(port=5000, debug = True)
