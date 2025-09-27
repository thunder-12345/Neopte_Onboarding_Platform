from project import db, app
from project.decorators import permission_required
from flask import render_template, redirect, request, url_for, flash 
from flask_login import login_user, login_required, logout_user
from project.models import User
from project.forms import RegistrationForm, LoginForm 
from distutils.log import debug
from fileinput import filename

#create first admin user
with app.app_context():
    # Only create if not already there
    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(
            name="Admin User",
            email="admin@example.com",
            password="admin123",   # hashed automatically in __init__
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@example.com / admin123")
    else:
        print("Admin user already exists")

@app.route("/upgrade/user", methods=["POST"])
@login_required
@permission_required('admin')
def upgrade_user():
    user_id = request.form.get("user_id", type=int)

    if not user_id:
        flash("No user selected.")
        return redirect(url_for("admin_dashboard"))
    
    user = User.query.get(user_id)

    if user is None:
        flash("User not found!")
        return redirect(url_for("admin_dashboard"))
    
    user.role = "admin"
    db.session.commit()
    flash(f"User {user.name} has been upgraded to admin.")
    return redirect(url_for("admin_dashboard"))


@app.route("/")
def user_dashboard():
    return render_template("user_home.html")

@app.route("/admin/dashboard")
@login_required
@permission_required('admin')
def admin_dashboard():
    user = User.query.all()
    return render_template("admin_home.html", user = user)

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)  
        return render_template("acknowledgement.html", name = f.filename)  
    
# @app.route("/welcome")
# @login_required
# def welcome():
#     return render_template("welcome.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
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


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            #Log in the user
            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            
            return redirect(url_for("user_dashboard"))
        
            # #next = request.args.get('next')

            # # So let's now check if that next exists, otherwise we'll go to
            # # the welcome page.
            # #if next == None or not next[0]=='/':
            #     next = url_for('welcome')

            # return redirect(next)
        
        else:
            if user is None:
                flash('Email does not exist.')
            else: 
                flash('Invalid email or password.')

    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have successfully logged out!")
    return redirect(url_for("user_dashboard"))

if __name__ == "__main__": 
    app.run(port=5000, debug = True)
