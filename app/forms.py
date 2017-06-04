from flask_wtf import FlaskForm
#from flask_wtf import Form as BaseForm
from wtforms import TextField, StringField, validators, IntegerField, SelectField
from wtforms.validators import Required

#for other os
from app.api.database.connect_db import connect_db

#for linux
"""
import sys
import os
#directory_user_cabinet = os.getcwd()
directory_user_cabinet="/home/raldenprog/CFT/the_best_service/hackaton_cft/app/api/database"
sys.path.insert(0, directory_user_cabinet)
from connect_db import connect_db
"""

class LoginForm(FlaskForm):
    login = TextField('login', validators=[Required()])
    password = TextField('password', validators=[Required()])


class Regform(FlaskForm):
    login = TextField('login', validators = [Required()])
    password = TextField('password', validators=[Required()])
    PasswordRepeat = TextField('PasswordRepeat', validators=[Required()])
    name = TextField('name', validators=[Required()])
    surname = TextField('surname', validators=[Required()])
    patronymic = TextField('patronymic', validators=[Required()])
    sex = TextField('sex', validators=[Required()])
    number_parents = TextField('number_parents', validators=[Required()])
    tel_number = TextField('tel_number', validators=[Required()])


class AddchildForm(FlaskForm):
    login = TextField('login', validators=[Required()])
    password = TextField('password', validators=[Required()])
    PasswordRepeat = TextField('PasswordRepeat', validators=[Required()])
    name = TextField('name', validators=[Required()])
    surname = TextField('surname', validators=[Required()])
    patronymic = TextField('patronymic', validators=[Required()])
    sex = TextField('sex', validators=[Required()])
    number_close = TextField('number_close', validators=[Required()])
    number_open = TextField('number_open', validators=[Required()])
    number_needs = TextField('number_needs', validators=[Required()])


class Addtaskform(FlaskForm):
    childrens = SelectField('children')
    description = StringField('description', [validators.Length(min=10, max=255)])
    coin = IntegerField('coin', [validators.NumberRange(min=1, max=500)])


class closetaskform(FlaskForm):
    tasks = SelectField('tasks')


class addregexform(FlaskForm):
    childrens = SelectField('children')
    description = StringField('description', [validators.Length(min=10, max=255)])

