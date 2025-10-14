# Imports
from project import db, app
from project.decorators import permission_required
from flask import render_template, redirect, request, url_for, flash 
from flask_login import login_user, login_required, logout_user, current_user
from project.models import User, Document, Hours
from project.forms import RegistrationForm, LoginForm, AddHoursForm
from distutils.log import debug
from fileinput import filename
import random
import os

# Mapping user roles to their dashboard route names
redirect_target = {
    "intern": "intern_dashboard",
    "volunteer": "volunteer_dashboard",
    "board": "board_dashboard",
    "admin": "admin_dashboard"
}

# List of possible user roles
roles = ["intern", "user", "volunteer", "board"]

# Generate 20 random users with different roles for initial data
users_data = []
for i in range(1, 21):
    name = f"User{i}"
    email = f"user{i}@example.com"
    password = f"pass{i}123"
    role = random.choice(roles)
    users_data.append({"name": name, "email": email, "password": password, "role": role})

# Create admin and real admin users if they don't exist, and add generated users to the database
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

    realAdmin = User.query.filter_by(email="realadmin@gmail.com").first()
    if not realAdmin:
        realAdmin = User(
            name="REAL ADMIN",
            email="realadmin@gmail.com",
            password="admin123",   # password hashed in User model
            role="admin"
        )
        print(realAdmin.role)
        db.session.add(realAdmin)
        db.session.commit()
        print("realAdmin user created: realadmin@gmail.com / admin123")

    for u in users_data:
        # Avoid duplicates
        if not User.query.filter_by(email=u["email"]).first():
            user = User(
                name=u["name"],
                email=u["email"],
                password=u["password"],
                role=u["role"]
            )
            db.session.add(user)
            print(f"Adding {u['name']} ({u['role']})")
    db.session.commit()
    print("20 users added successfully!")

# Route to upgrade a user's role (accessible by board and admin roles)
@app.route("/upgrade/user", methods=["POST"])
@login_required
@permission_required('board')
def upgrade_user():
    user_id = request.form.get("user_id", type=int)  # Get user ID from form
    role_choice = request.form.get("role_choice", type=str)  # Get new role

    if not user_id:
        flash("No user selected.")
        return redirect(url_for(redirect_target.get(current_user.role, "user_dashboard")))
    
    user = User.query.get(user_id)  # Find user by ID

    if user is None:
        flash("User not found!")
        return redirect(url_for(redirect_target.get(current_user.role, "user_dashboard")))
    
    user.role = role_choice  # Update user role
    db.session.commit()
    flash(f"User {user.name} has been changed to {user.role} .")
    return redirect(url_for(redirect_target.get(current_user.role, "board_dashboard")))

# Route to delete a user (accessible by board and admin roles)
@app.route("/delete/user", methods=["POST"])
@login_required
@permission_required('board')
def delete_user():
    user_id = request.form.get("user_id", type=int)  # Get user ID from form
    user_name = request.form.get("user_name", type=str) 

    if not user_id:
        flash("No user selected.")
        return redirect(url_for(redirect_target.get(current_user.role, "user_dashboard")))
    
    user = User.query.get(user_id)  # Find user by ID

    if user is None:
        flash("User not found!")
        return redirect(url_for(redirect_target.get(current_user.role, "user_dashboard")))
    
    db.session.delete(user)  # Delete user from database
    db.session.commit()
    flash(f"User {user_name} has been deleted.")
    return redirect(url_for(redirect_target.get(current_user.role, "board_dashboard")))
    
# Home page for general users (no login required)
@app.route("/")
def user_dashboard():
    return render_template("user_home.html")

# Dashboard for interns (intern role only)
@app.route("/intern/dashboard")
@login_required
@permission_required('intern')
def intern_dashboard():
    return render_template("intern_home.html")

# Dashboard for volunteers (volunteer role only)
@app.route("/volunteer/dashboard")
@login_required
@permission_required('volunteer')
def volunteer_dashboard():
    return render_template("volunteer_home.html")

# Dashboard for board members (board role only)
@app.route("/board/dashboard")
@login_required
@permission_required('board')
def board_dashboard():
    user = User.query.all()  # Get all users
    return render_template("board_home.html", user = user)

# Dashboard for admin (admin role only)
@app.route("/admin/dashboard")
@login_required
@permission_required('admin')
def admin_dashboard():
    user = User.query.all()  # Get all users
    return render_template("admin_home.html", user = user)

@app.route("/specific/log/hours", methods=["GET", "POST"])
@login_required
@permission_required('volunteer')
def specific_log_hours():
    user_id = request.args.get('user_id') or request.form.get('user_id')

    if user_id:
        user = User.query.get(user_id)
        if user:
            return render_template('specific_user_hours_log.html', user=user)
        else:
            flash("User not found.")
            return redirect(url_for(redirect_target.get(current_user.role, "user_dashboard")))
    
    # For volunteer/intern viewing their own hours
    return render_template('specific_user_hours_log.html')

# create a specific users hours log view 
    # volunteer/intern view
        # table to view their own hours previously added
    # board/admin view 
        # view the specific user's hours log table selected with status change ability

# create a hours log view w dif permissions for each role 
    # volunteer/intern view (Navbar says Add Hours)
        # form to add hours and other details
        # button to click to view their own hours previously added - routes to specific_user_hours 
    # board/admin view (Navbar says View Hours)
        # select user from user list to view their hours logged in a table including status change ability

        # DO THIS!! seperate table to view all pending hours with ability to approve/deny (similar to notifications) - do this for documents too
@app.route("/hours/log", methods=["GET", "POST"])
@login_required
@permission_required('volunteer')
def hours_log():
    if current_user.role in ['volunteer', 'intern']:
        form = AddHoursForm()  # Create form to add hours
    
        if request.method == "POST":
            if form.validate_on_submit():  # If form is valid
                log = Hours(
                    activity_name=form.data['activity_name'],
                    date=form.data['date'],
                    start_time=form.data['start_time'],
                    end_time=form.data['end_time'],
                    amount=form.data['amount'],
                    description=form.data['description'],
                    user=current_user
                )
                db.session.add(log)
                db.session.commit()
                flash("You have logged your hours!")
                return redirect(url_for('specific_log_hours'))
            else:
                flash("Error")
                print("Form errors:", form.errors)

        # Return template on GET or if form fails validation
        return render_template("hours_log.html", form=form)
    
    else:  # board or admin
        users = User.query.all()
        return render_template("hours_log.html", users=users)

@app.route("/hours/log/update_status/", methods=["POST"])
@login_required
@permission_required('board')    
def update_hours_log_status():
    log_id = request.form.get("log_id", type=int)  
    new_status = request.form.get("new_status", type=str)  
    log = Hours.query.get(log_id)
    if log:
        log.status = new_status
        db.session.commit()
    return redirect(url_for('specific_log_hours', user_id=log.user_id))

# if volunteer or intern, view the documents they've uploaded and their status
# if board or admin, view all documents and status and ability to change their status
@app.route("/documents/status", methods = ["GET", "POST"])
@login_required
@permission_required('volunteer')
def document_status():
    # handle file uploads
    if request.method == 'POST':  
        uploaded_files = request.files.getlist('file')  # note: 'file' is the input name
        saved_files = []
    
        for f in uploaded_files:
            if f.filename:  # skip empty uploads
                if not allowed_file(f.filename):
                    return render_template( "document_status_list.html", 
                                           names=saved_files, 
                                           msg="File extension not allowed", 
                                           allGood = False, justTriedUpload=True) 
                    
        for f in uploaded_files:
            if f.filename:  # skip empty uploads
                f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
                saved_files.append(f.filename)
                description = request.form.get("description", type=str)  # Get description from form
                document = Document(
                    filename=f.filename,
                    doctype=f.content_type,
                    description = description,
                    user=current_user
                )
                db.session.add(document)
                db.session.commit()
                                    
        return render_template("document_status_list.html", 
                               names=saved_files, 
                               msg="File(s) uploaded successfully", 
                               allGood = True, justTriedUpload=True)
    
    if current_user.role in ['volunteer', 'intern']:
        documents = Document.query.filter_by(user_id=current_user.id).all()
        return render_template("document_status_list.html", documents=documents, role=current_user.role)
    else:  # board or admin
        documents = Document.query.all()
        users = User.query.all()
        return render_template("document_status_list.html", documents=documents, users=users, role=current_user.role)
    
@app.route("/documents/update_status/", methods=["POST"])
@login_required
@permission_required('board')    
def update_document_status():
    doc_id = request.form.get("doc_id", type=int)  
    new_status = request.form.get("new_status", type=str)  
    document = Document.query.get(doc_id)
    if document:
        document.status = new_status
        db.session.commit()
    return redirect(url_for('document_status'))
        
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']
    
@app.route("/specific/log/document", methods=["GET", "POST"])
@login_required
@permission_required('volunteer')
def specific_log_document():
    user_id = request.args.get('user_id') or request.form.get('user_id')

    if user_id:
        user = User.query.get(user_id)
        if user:
            return render_template('specific_user_document.html', user=user)
        else:
            flash("User not found.")
            return redirect(url_for(redirect_target.get(current_user.role, "user_dashboard")))
    
    # For volunteer/intern viewing their own document
    return render_template('specific_user_document.html', user=current_user)
    
# Registration route (handles user registration)
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

# Login route (handles user login)
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
            return redirect(url_for(redirect_target.get(current_user.role, "user_dashboard")))
        
        else:
            if user is None:
                flash('Email does not exist.')
            else: 
                flash('Invalid email or password.')

    return render_template('login.html', form=form)

# Logout route (logs out the current user)
@app.route("/logout")
@login_required
def logout():
    logout_user()  # Log out user
    flash("You have successfully logged out!")
    return redirect(url_for("user_dashboard"))

# Run the app if this file is executed directly
if __name__ == "__main__": 
    app.run(port=5000, debug = True)
