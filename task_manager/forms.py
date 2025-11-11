from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired , length, Email, EqualTo,ValidationError, Optional
from task_manager.models import User

#Registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=2, max = 25)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('Sign up')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken use another one')
        
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('An account with that email already exists')
#login
class LoginForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Login')

#profile edit
class EditProfile(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=2, max = 25)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is taken use another one')
        
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('An account with that email already exists')

#Tasks         
class TaskForm(FlaskForm):
    title = StringField('title', validators=[(DataRequired()), length(max=100)])
    deadline = DateField('deadline', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Add Task')