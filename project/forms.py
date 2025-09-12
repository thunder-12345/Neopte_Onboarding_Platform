from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

from project.models import User

class RegistrationForm(FlaskForm): 
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators = [DataRequired(), EqualTo('confirm_pass', message='Passwords Must Match!')])
    confirm_pass = PasswordField("Confirm Password: ", validators = [DataRequired(), EqualTo("password", message = "The passwords must match.")])
    submit = SubmitField("Register")

    #check if email is unique 
    def validate_email(self, email):
        if User.query.filter_by(email = self.email.data).first():
            raise ValidationError("An account with this email already exists.")
    
class LoginForm(FlaskForm): 
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators = [DataRequired()])
    submit = SubmitField("Login")


