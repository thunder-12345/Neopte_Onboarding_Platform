from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional, Length
from wtforms import ValidationError
from wtforms.fields import DateField, FileField, TextAreaField, SelectField, SelectMultipleField, BooleanField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms_components import TimeField
from project.models import User
from datetime import date

class RegistrationForm(FlaskForm): 
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators = [DataRequired(), EqualTo('confirm_pass', message='Passwords Must Match!')])
    confirm_pass = PasswordField("Confirm Password: ", validators = [DataRequired(), EqualTo("password", message = "The passwords must match.")])
    submit = SubmitField("Register")

    def validate_name(self, field):
        if any(char.isdigit() for char in field.data):
            raise ValidationError("Name cannot contain numbers.")
        
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

class CreateTasksForm(FlaskForm):
    """Form for creating a new task (Step 1)"""
    
    title = StringField(
        'Task Title', 
        validators=[DataRequired(), Length(min=3, max=200)]
    )
    
    description = TextAreaField(
        'Description', 
        validators=[DataRequired(), Length(min=0, max=1000)]
    )
    
    # Only 2 classification options: project and reminder
    classification = SelectField(
        'Classification',
        choices=[
            ('', '-- Select Classification --'),
            ('project', 'Project'),
            ('reminder', 'Reminder')
        ],
        validators=[DataRequired(message="Please select a classification")]
    )
    
    # 4 role options: intern, volunteer, board, OR specific users
    assigned_role = SelectField(
        'Assign To',
        choices=[
            ('specific', 'Specific Users (Choose in Next Step)'),  # ← This triggers user selection
            ('intern', 'All Interns'),
            ('volunteer', 'All Volunteers'),
            ('board', 'All Board Members')
            
        ],
        validators=[DataRequired(message="Please select who to assign this to")]
    )
    
    submit = SubmitField('Continue to Assignment')


class CreateTaskAssignmentForm(FlaskForm):
    """Form for assigning a task to users (Step 2)"""
    
    def not_in_past(form, field):
        if field.data < date.today():
            raise ValidationError("Due date cannot be in the past.")
        
    due_date = DateField(
        'Due Date', 
        validators=[DataRequired(message="Please select a due date"),
                    not_in_past]
    )
    
    upload_required = BooleanField(
        'Upload Required',
        default=False
    )
    
    # Multi-select for specific users (only shown when assigned_role == 'specific')
    users_selected = SelectMultipleField(
        'Select Specific Users',
        coerce=int,  # Converts string IDs to integers
        validators=[Optional()],
        choices=[]  # Set dynamically in the route
    )
    
    submit = SubmitField('Complete Task Creation')

    