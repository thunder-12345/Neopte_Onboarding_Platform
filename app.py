from project import db, app
from flask import render_template, redirect, request, url_for, flash 
from flask_login import login_user, login_required, logout_user
from project.models import User
from project.forms import RegistrationForm, LoginForm 

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/welcome")
@login_required
def welcome():
    return render_template("welcome.html")

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
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome')

            return redirect(next)
        
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
    return redirect(url_for("home"))

if __name__ == "__main__": 
    app.run(debug = True)
