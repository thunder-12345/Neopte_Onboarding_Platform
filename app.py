# Imports
from project import db, app
from project.decorators import permission_required
from flask import render_template, redirect, request, url_for, flash, send_from_directory, send_file, current_app, session
from flask_login import login_user, login_required, logout_user, current_user
from project.models import User, Document, Hours, ActivityLog, Task, TaskAssignment
from project.forms import RegistrationForm, LoginForm, AddHoursForm, EditProfile, CreateTasksForm, CreateTaskAssignmentForm
from project.activity import log_event

from fileinput import filename
import random
import os
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
from datetime import datetime


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
            picture="default.jpeg",
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
                role=u["role"], 
                picture="default.jpeg",
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
    
    old_role = user.role
    user.role = role_choice # Update user role

    log_event(
        actor=current_user,
        action="user_role_changed",
        target_type="User",
        target_id=user.id,
        details={
            "old_role": old_role,
            "new_role": role_choice
        }
    )
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
    
    log_event(
        actor=current_user,
        action="user_deleted",
        target_type="User",
        target_id=user.id,
        details={
            "email": user.email,
            "role": user.role
        }
    )

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
                log_event(
                    actor=current_user,
                    action="hours_created",
                    target_type="Hours",
                    target_id=log.id, #must commit previously to get id
                    details={
                        "activity_name": log.activity_name,
                        "amount": log.amount,
                        "date": str(log.date)
                    }
                )
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
    old_status = log.status
    if log:

        if new_status == "Approved":
            user = User.query.get(log.user_id)
            user.total_hours += log.amount
            
            log_event(
                actor=current_user,
                action="hours_status_changed",
                target_type="Hours",
                target_id=log.id,
                details={
                    "old_status": old_status,
                    "new_status": new_status,
                    "amount": log.amount,
                    "user_id": log.user_id
                }
            )

        elif log.status == "Approved" and new_status in ["Denied", "Pending"]:
            user = User.query.get(log.user_id)
            user.total_hours -= log.amount


            log_event(
                actor=current_user,
                action="hours_status_changed",
                target_type="Hours",
                target_id=log.id,
                details={
                    "old_status": old_status,
                    "new_status": new_status,
                    "amount": log.amount,
                    "user_id": log.user_id
                }
            )

        log.status = new_status
        db.session.commit()

    return redirect(request.referrer or url_for('specific_log_hours', user_id=log.user_id))

@app.route('/pending/hours', methods=['GET'])
@login_required
@permission_required('board')
def pending_hours():
    users = User.query.all()  # Get all users
    return render_template('pending_hours.html', users= users)

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

                log_event(
                    actor=current_user,
                    action="document_uploaded",
                    target_type="Document",
                    target_id=document.id,
                    details={
                        "filename": document.filename,
                        "doctype": document.doctype
                    }
                )
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
    old_status = document.status
    if document:
        log_event(
            actor=current_user,
            action="document_status_changed",
            target_type="Document",
            target_id=document.id,
            details={
                "old_status": old_status,
                "new_status": new_status
            }
        )
        document.status = new_status
        db.session.commit()
    return redirect(request.referrer or url_for('document_status'))
        
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']
    
@app.route("/specific/log/document", methods=["GET", "POST"])
@login_required
@permission_required('volunteer')
def specific_log_document():
    user_id = request.args.get('user_id') or request.form.get('user_id')
    from_pending = request.args.get('from_pending', type=bool, default=False)
    if from_pending:
        return redirect(url_for('pending_documents'))
    if user_id:
        user = User.query.get(user_id)
        if user:
            return render_template('specific_user_document.html', user=user)
        else:
            flash("User not found.")
            return redirect(url_for(redirect_target.get(current_user.role, "user_dashboard")))
    
    # For volunteer/intern viewing their own document
    return render_template('specific_user_document.html', user=current_user)

@app.route('/view/<int:doc_id>', methods=['GET'])
@login_required
@permission_required('board')
def view_pdf(doc_id):
    doc = Document.query.get_or_404(doc_id)
    path = os.path.join(app.config['UPLOAD_PATH'], doc.filename)
    return send_file(
        path,
        mimetype='application/pdf',
        download_name=f'{doc.filename}.pdf',
        as_attachment=False  # <-- makes it open inline
    )

    # doc = Document.query.get_or_404(doc_id)
    # user_id = request.args.get('user_id')
    # user = User.query.get(user_id)
    # from_pending = request.args.get('from_pending', type=bool, default=False)
    # return render_template('view_pdf.html', doc=doc, user = user, from_pending=from_pending)

# @app.route('/uploads/<filename>')
# @login_required
# @permission_required('board')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/pending/documents', methods=['GET'])
@login_required
@permission_required('board')
def pending_documents():
    users = User.query.all()  # Get all users
    return render_template('pending_documents.html', users= users)

@app.route("/notification")
@login_required
@permission_required('board')
def notification():
    logs = (
        ActivityLog.query
        .order_by(ActivityLog.created_at.desc())
        .limit(100)
        .all()
    )
    return render_template("notification.html", logs=logs)

@login_required
@app.route("/edit/profile", methods=["GET", "POST"])
def edit_profile():
    form = EditProfile()  # Create form to edit profile

    if request.method == "POST":

        changed_fields = {}

        if form.validate_on_submit():  # If form is valid
            
            if form.data['name'] and form.data['name'] != current_user.name:
                changed_fields['name'] = form.data['name']
                current_user.name = form.data['name']

            if form.data['email'] and form.data['email'] != current_user.email:
                changed_fields['email'] = form.data['email']
                current_user.email=form.data['email']

            if form.data['address'] and form.data['address'] != current_user.address:
                changed_fields['address'] = form.data['address']
                current_user.address=form.data['address']

            if form.picture.data:
                file = form.picture.data
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.root_path, 'static/profile_pics', filename))
                current_user.picture = filename
                changed_fields['picture'] = filename

            if changed_fields:  # Only log if something actually changed
                log_event(
                    actor=current_user,
                    action="profile_updated",
                    target_type="User",
                    target_id=current_user.id,
                    details=changed_fields
                )
                db.session.commit()
            
            return redirect(url_for('edit_profile'))
        else:
            flash("Error")
            print("Form errors:", form.errors)

    # Return template on GET or if form fails validation
    return render_template("edit_profile.html", form = form)

@login_required
@permission_required('board')
@app.route("/user/list")
def user_list():
    if request.args.get('filter_by') and request.args.get('search_query'):
        filter_by = request.args.get('filter_by')
        search_query = request.args.get('search_query')
        
        if filter_by == 'role':
            # Filter by role
            users = User.query.filter(User.role.ilike(f'%{search_query}%')).all()
        elif filter_by == 'name':
            # Filter by name
            users = User.query.filter(User.name.ilike(f'%{search_query}%')).all()
    else:
        # No filter, show all users
        users = User.query.all()    
    
    return render_template("user_list.html", users=users)

    
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
            # flash('Logged in successfully.')

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
    # flash("You have successfully logged out!")
    return redirect(url_for("user_dashboard"))


@login_required
@permission_required('volunteer')
def generate_volunteer_certificate(user):
    """
    Generate a professional volunteer certificate PDF.
    
    What this does:
    1. Creates a PDF in memory (BytesIO buffer)
    2. Draws a professional certificate with borders
    3. Fills in the volunteer's name, start date, and total hours
    4. Returns the PDF buffer ready to send
    
    Args:
        user: A User object from your database
    
    Returns:
        BytesIO buffer containing the PDF data
    """

    # Create PDF in memory (not on disk!)
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # 612 x 792 points (8.5" x 11")
    
    # ---------------------------
    # OUTER BORDER
    # ---------------------------
    pdf.setStrokeColor(colors.HexColor('#2C3E50'))  # Dark blue-gray
    pdf.setLineWidth(3)
    pdf.rect(0.5 * inch, 0.5 * inch, width - 1*inch, height - 1*inch)
    
    # Inner decorative border
    pdf.setLineWidth(1)
    pdf.rect(0.6 * inch, 0.6 * inch, width - 1.2*inch, height - 1.2*inch)
    
    # ---------------------------
    # HEADER SECTION WITH LOGO
    # ---------------------------
    y_pos = height - 1 * inch
    
    # Add logo image at the top - stretched nearly border to border
    logo_path = os.path.join(app.root_path, 'static', 'neopte logo.jpeg')
    if os.path.exists(logo_path):
        # Logo dimensions - stretched almost to borders
        logo_width = width - 1.4 * inch  # Stops just before the inner border
        logo_height = 1.5 * inch  # Adjust height as needed
        logo_x = 0.7 * inch  # Start just after the inner border
        
        pdf.drawImage(logo_path, logo_x, y_pos - logo_height, 
                     width=logo_width, height=logo_height, 
                     preserveAspectRatio=True, mask='auto')
        
        y_pos -= logo_height + 0.5 * inch
    else:
        # Fallback to text if logo not found
        pdf.setFont("Helvetica-Bold", 28)
        pdf.setFillColor(colors.HexColor('#2C3E50'))
        title = "Neopte Foundation"
        title_width = pdf.stringWidth(title, "Helvetica-Bold", 28)
        pdf.drawString((width - title_width) / 2, y_pos, title)
        y_pos -= 0.8 * inch
    
    # ---------------------------
    # MAIN CONTENT - THE VOLUNTEER INFO
    # ---------------------------
    pdf.setFont("Helvetica", 14)
    pdf.setFillColor(colors.black)
    
    # "This certifies that"
    intro = "This certifies that"
    intro_width = pdf.stringWidth(intro, "Helvetica", 14)
    pdf.drawString((width - intro_width) / 2, y_pos, intro)
    
    y_pos -= 0.7 * inch
    
    # VOLUNTEER NAME - The star of the show!
    pdf.setFont("Helvetica-Bold", 24)
    pdf.setFillColor(colors.HexColor('#3498DB'))  # Blue
    name_width = pdf.stringWidth(user.name, "Helvetica-Bold", 24)
    pdf.drawString((width - name_width) / 2, y_pos, user.name)
    
    # Underline the name for emphasis
    pdf.setStrokeColor(colors.HexColor('#3498DB'))
    pdf.setLineWidth(1)
    pdf.line((width - name_width) / 2 - 10, y_pos - 5, 
             (width + name_width) / 2 + 10, y_pos - 5)
    
    y_pos -= 0.8 * inch
    
    # Service description with start date
    pdf.setFont("Helvetica", 14)
    pdf.setFillColor(colors.black)
    
    # Format the start date
    
    if user.date_created:
        start_date = user.date_created.strftime('%B %d, %Y')
        service_text = f"has been serving with the Neopte Foundation since {start_date}"
    else:
        service_text = "has been serving with the Neopte Foundation"
    
    service_width = pdf.stringWidth(service_text, "Helvetica", 14)
    pdf.drawString((width - service_width) / 2, y_pos, service_text)
    
    y_pos -= 0.8 * inch
    
    # Hours intro
    hours_intro = "contributing a total of"
    hours_intro_width = pdf.stringWidth(hours_intro, "Helvetica", 14)
    pdf.drawString((width - hours_intro_width) / 2, y_pos, hours_intro)
    
    y_pos -= 0.6 * inch
    
    # TOTAL HOURS - Big and bold!
    pdf.setFont("Helvetica-Bold", 22)
    pdf.setFillColor(colors.HexColor('#E74C3C'))  # Red for emphasis
    hours_text = f"{user.total_hours:.1f} volunteer hours"
    hours_width = pdf.stringWidth(hours_text, "Helvetica-Bold", 22)
    pdf.drawString((width - hours_width) / 2, y_pos, hours_text)
    
    y_pos -= 1.5 * inch
    
    # ---------------------------
    # FOOTER - Gratitude message
    # ---------------------------
    pdf.setFont("Helvetica-Oblique", 11)
    pdf.setFillColor(colors.HexColor('#7F8C8D'))
    gratitude = "We deeply appreciate your dedication and service to our community."
    gratitude_width = pdf.stringWidth(gratitude, "Helvetica-Oblique", 11)
    pdf.drawString((width - gratitude_width) / 2, y_pos, gratitude)
    
    y_pos -= 1 * inch
    
    # Signature line
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    sig_start = width / 2 - 2 * inch
    pdf.line(sig_start, y_pos, sig_start + 4*inch, y_pos)
    
    y_pos -= 0.3 * inch
    
    # Signature label
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(colors.black)
    sig_label = "Executive Director, Neopte Foundation"
    sig_width = pdf.stringWidth(sig_label, "Helvetica", 10)
    pdf.drawString((width - sig_width) / 2, y_pos, sig_label)
    
    # ---------------------------
    # METADATA - Bottom of page
    # ---------------------------
    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(colors.HexColor('#BDC3C7'))  # Light gray
    
    # Certificate ID (bottom right)
    cert_id = f"Certificate ID: NF-{user.id:05d}"
    pdf.drawString(width - 2.5*inch, 0.7*inch, cert_id)
    
    # Issue date (bottom left)
    issue_date = datetime.now().strftime('%B %d, %Y')
    pdf.drawString(0.7*inch, 0.7*inch, f"Issued: {issue_date}")
    
    # Finalize the PDF
    pdf.showPage()
    pdf.save()
    
    # Reset buffer to beginning so it can be read
    buffer.seek(0)
    return buffer

@app.route('/certificate/view')
@login_required
@permission_required('volunteer')
def view_certificate():
    """
    View certificate in browser.
    
    How this works:
    - Volunteers/interns see their own certificate
    - Board/admin can view any user's certificate by passing ?user_id=X
    
    Example URLs:
    - /certificate/view (volunteer sees their own)
    - /certificate/view?user_id=5 (board views user #5's certificate)
    """
    # Determine which user's certificate to show
    if current_user.role in ['board', 'admin']:
        # Board/admin can specify a user_id
        user_id = request.args.get('user_id', type=int)
        if user_id:
            user = User.query.get_or_404(user_id)
        else:
            flash("No user specified.")
            return redirect(url_for(redirect_target.get(current_user.role)))
    else:
        # Volunteers/interns only see their own
        user = current_user
    
    # Generate the PDF
    pdf_buffer = generate_volunteer_certificate(user)
    
    # Send it to the browser (opens in new tab)
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=False,  # False = open in browser
        download_name=f'neopte_certificate_{user.name.replace(" ", "_")}.pdf'
    )

@app.route('/certificate/download')
@login_required
@permission_required('volunteer')
def download_certificate():
    """
    Download certificate to computer.
    
    This is identical to view_certificate() except as_attachment=True
    which tells the browser to download instead of display.
    """
    # Same user determination logic
    if current_user.role in ['board', 'admin']:
        user_id = request.args.get('user_id', type=int)
        if user_id:
            user = User.query.get_or_404(user_id)
        else:
            flash("No user specified.")
            return redirect(url_for(redirect_target.get(current_user.role)))
    else:
        user = current_user
    
    # Generate the PDF
    pdf_buffer = generate_volunteer_certificate(user)
    
    # Send it as a download
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,  # True = force download
        download_name=f'neopte_volunteer_certificate_{user.name.replace(" ", "_")}.pdf'
    )

@app.route("/policies", methods=["GET"])
@login_required
@permission_required('volunteer')
def policies():
    return render_template("policies.html")

@app.route("/create/task", methods=["GET", "POST"])
@login_required
@permission_required('board')
def create_task():
    from flask import session
    
    # Step 1: Create the basic task
    if 'task_id' not in session:
        form = CreateTasksForm()
        
        if request.method == "POST" and form.validate_on_submit():
            # Create the task with selected classification and assigned_role
            task = Task(
                title=form.data['title'],
                description=form.data['description'],
                classification=form.data['classification'],  # 'project' or 'reminder'
                assigned_role=form.data['assigned_role'],    # 'intern', 'volunteer', 'board', or 'specific'
                created_by=current_user
            )
            db.session.add(task)
            db.session.commit()
            
            log_event(
                actor=current_user,
                action="task_created",
                target_type="Task",
                target_id=task.id,
                details={
                    "title": task.title,
                    "classification": task.classification,
                    "assigned_role": task.assigned_role
                }
            )
            db.session.commit()
            
            # Store task info in session for step 2
            session['task_id'] = task.id
            session['assigned_role'] = task.assigned_role
            
            flash("Task created! Now set the assignment details.")
            return redirect(url_for('create_task'))
        
        return render_template("create_task.html", form=form, step=1)
    
    # Step 2: Assign the task to users
    else:
        task_id = session.get('task_id')
        assigned_role = session.get('assigned_role')
        task = Task.query.get(task_id)
        
        if not task:
            session.pop('task_id', None)
            session.pop('assigned_role', None)
            flash("Task not found. Please try again.")
            return redirect(url_for('create_task'))
        
        form2 = CreateTaskAssignmentForm()
        
        # Get users based on assigned_role
        if assigned_role in ['intern', 'volunteer', 'board']:
            # Get users with that specific role (for read-only display)
            users = User.query.filter_by(role=assigned_role).all()
        elif assigned_role == 'specific':
            # Get ALL users for the multi-select dropdown
            users = User.query.all()
            # Populate the dropdown choices
            form2.users_selected.choices = [(u.id, f"{u.name} ({u.email})") for u in users]
        else:
            users = []
        
        if request.method == "POST" and form2.validate_on_submit():
            due_date = form2.data['due_date']
            upload_required = form2.data['upload_required']
            
            if assigned_role in ['intern', 'volunteer', 'board']:
                # Assign to ALL users with that role
                users_to_assign = User.query.filter_by(role=assigned_role).all()
                
                for user in users_to_assign:
                    assignment = TaskAssignment(
                        task=task,
                        user=user,
                        due_date=due_date,
                        upload=upload_required
                    )
                    db.session.add(assignment)
            
            elif assigned_role == 'specific':
                # Assign to SELECTED users only
                user_ids = form2.users_selected.data
                users_selected = User.query.filter(User.id.in_(user_ids)).all()
                
                if not users_selected:
                    flash("Please select at least one user to assign the task to.")
                    return render_template("create_task.html", 
                                         form2=form2, 
                                         step=2, 
                                         task=task, 
                                         users=users,
                                         assigned_role=assigned_role)
                
                for user in users_selected:
                    assignment = TaskAssignment(
                        task=task,
                        user=user,
                        due_date=due_date,
                        upload=upload_required
                    )
                    db.session.add(assignment)
            
            db.session.commit()
            
            # Clear session
            session.pop('task_id', None)
            session.pop('assigned_role', None)
            
            flash(f"Task has been created and assigned successfully!")
            return redirect(url_for('create_task'))
        
        return render_template("create_task.html", 
                             form2=form2, 
                             step=2, 
                             task=task, 
                             users=users,
                             assigned_role=assigned_role)

# Optional: Route to cancel task creation and go back to step 1
@app.route("/create/task/cancel", methods=["POST"])
@login_required
@permission_required('board')
def cancel_task_creation():
    from flask import session
    
    task_id = session.get('task_id')
    if task_id:
        # Delete the incomplete task
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
    
    session.pop('task_id', None)
    session.pop('assigned_role', None)
    
    flash("Task creation cancelled.")
    return redirect(url_for('create_task'))

# Run the app if this file is executed directly
if __name__ == "__main__": 
    app.run(port=5000, debug = True)
