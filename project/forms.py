from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional
from wtforms import ValidationError
from wtforms.fields import DateField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms_components import TimeField
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

class EditProfile(FlaskForm): 
    name = StringField("Edit Name: ")
    email = StringField("Edit Email: ", validators=[Optional(), Email()])
    address = StringField("Edit Address: ")
    picture = FileField("Profile Picture: ", validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField("Submit Changes")

class AddHoursForm(FlaskForm):
    activity_name = StringField("Activity Name: ", validators=[DataRequired()])
    date = DateField('Date:', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField("Start Time: ", validators=[DataRequired()])
    end_time = TimeField("End Time: ", validators=[DataRequired()])
    amount = FloatField("Amount of Hours: ", validators=[DataRequired(), NumberRange(0, 24, "Must be between 0 and 24 hours") ])
    description = StringField("Description: ", validators=[DataRequired()])
    submit = SubmitField("Add Hours")

