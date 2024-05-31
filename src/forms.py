from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, SelectField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from database import Weekday


#User
# class CreateUserForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     name = StringField('Name', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
#     submit = SubmitField('Create')
    
class UpdateUserForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional()])
    name = StringField('Name', validators=[Optional()])
    password = PasswordField('Password', validators=[Optional()])
    is_superuser = BooleanField('Superuser', validators=[Optional()])
    updateusersubmit = SubmitField('Update', validators=[Optional()])

class DeleteUserForm(FlaskForm):
    id = IntegerField('Id')
    deleteusersubmit = SubmitField('Delete')


#Channel
class CreateChannelForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    createchannelsubmit = SubmitField('Create')

class UpdateChannelForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    updatechannelsubmit = SubmitField('Update')
    
class DeleteChannelForm(FlaskForm):
    id = IntegerField('Id')
    deletechannelsubmit = SubmitField('Delete')


#Program
class CreateProgramForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    weekday = SelectField('Weekday', choices=[(day.name, day.value) for day in Weekday], validators=[DataRequired()])
    channel_id = IntegerField('Channel', validators=[DataRequired()])
    createprogramsubmit = SubmitField('Create')

class UpdateProgramForm(FlaskForm):
    programid = IntegerField('Id', validators=[DataRequired()])
    title = StringField('Title', validators=[Optional()])
    start_time = TimeField('Start Time', validators=[Optional()])
    weekday = SelectField('Weekday', choices=[('', '')]+[(day.name, day.value) for day in Weekday], validators=[Optional()])
    channel_id = IntegerField('Channel', validators=[Optional()])
    updateprogramsubmit = SubmitField('Update')

class DeleteProgramForm(FlaskForm):
    id = IntegerField('Id')
    deleteprogramsubmit = SubmitField('Delete')
