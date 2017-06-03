from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class LoginForm(Form):
    login = TextField('login', validators=[Required()])
    password = TextField('password', validators=[Required()])


class Regform(Form):
    login = TextField('login', validators = [Required()])
    password = TextField('password', validators=[Required()])
    PasswordRepeat = TextField('PasswordRepeat', validators=[Required()])
    name = TextField('name', validators=[Required()])
    surname = TextField('surname', validators=[Required()])
    patronymic = TextField('patronymic', validators=[Required()])
    sex = TextField('sex', validators=[Required()])
    number_parents = TextField('number_parents', validators=[Required()])
    tel_number = TextField('tel_number', validators=[Required()])


class AddchildForm(Form):
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


class Addtaskform(Form):
    description= TextField('description', validators=[Required()])
    coin = TextField('coin', validators=[Required()])
