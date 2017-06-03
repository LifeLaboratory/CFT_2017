from app import app
from flask import Flask, request, redirect, url_for
from flask import render_template, flash, redirect
from app.check_parents_and_children import check_login
from app.forms import LoginForm
from app.forms import Regform
from app.forms import AddchildForm
from flask import make_response, session
from create_parent import create_parent
from create_children import create_child
from login_manager import login_in
import uuid
import sqlite3



@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    if request.method == 'GET':
        return render_template("index.html",
                                )



@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    form = Regform()
    if form.validate_on_submit():
        if form.password.data == form.PasswordRepeat.data:
            answer_check = check_login(form.login.data)
            if answer_check != 0:
                return answer_check
            else:
                balance_needs = 0
                balance_close = 0
                balance_open = 0
                balance_parent = 0
                create_parent(form.login.data, form.password.data, form.name.data,
                            form.surname.data, form.patronymic.data, form.sex.data, form.number_parents.data,
                              balance_needs, balance_close, balance_open,
                              balance_parent, form.tel_number.data,)
                return redirect('/index')
        else:
            return "Passwords do not match"
    return render_template('registration.html',
        title = 'Sign In',
        form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        answer = login_in(form.login.data, form.password.data)
        if  answer== "NO":
            return "Wrong password or login"
        else:
            session['login'] = form.login.data
            session['id_parent'] = answer
            return "YES"
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/add_child', methods = ['GET', 'POST'])
def add_child():
    form = AddchildForm()
    if form.validate_on_submit():
        uid_parent = session['id_parent']
        create_child(uid_parent, form.login.data, form.password.data, form.name.data,
                      form.surname.data, form.patronymic.data, form.sex.data, form.number_close.data,
                      form.number_open.data, form.number_needs.data)
        return redirect('/index')
    return render_template('add_child.html',
                           title='Sign In',
                           form=form)

'''
@app.route('/add_task', methods = ['GET', 'POST'])
def add_task():
    form = AddchildForm()
    if form.validate_on_submit():

'''