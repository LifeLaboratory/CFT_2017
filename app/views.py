from app import app
from flask import Flask, request, redirect, url_for
from flask import render_template, flash, redirect
from app.check_parents_and_children import check_login
from app.forms import LoginForm
from app.forms import Regform, closetaskform
from app.forms import AddchildForm, Addtaskform
from flask import make_response, session


# for other os
from app.api.database.connect_db import connect_db
from app.api.database.create_parent import create_parent
from app.api.database.create_task import create_task
from app.api.database.create_children import create_child
from app.api.database.login_manager import login_in


# for linux
"""
import sys
import os
#directory_user_cabinet = os.getcwd()
directory_user_cabinet="/home/raldenprog/CFT/the_best_service/hackaton_cft/app/api/database"
sys.path.insert(0, directory_user_cabinet)
from create_parent import create_parent
from create_children import create_child
from login_manager import login_in
"""

@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    if request.method == 'GET':
        return render_template("index.html")


@app.route('/registration', methods=['GET', 'POST'])
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
        title='Sign In',
        form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = login_in(form.login.data, form.password.data)
        if data['id'] == "Error":
            return "Wrong password or login"
        else:
            session['login'] = form.login.data
            session['id'] = data['id']
            session['status'] = data['status']
            return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/add_child', methods=['GET', 'POST'])
def add_child():
    form = AddchildForm()
    if form.validate_on_submit():
        uid_parent = session['id']
        create_child(uid_parent, form.login.data, form.password.data, form.name.data,
                      form.surname.data, form.patronymic.data, form.sex.data, form.number_close.data,
                      form.number_open.data, form.number_needs.data)
        return redirect('/index')
    return render_template('add_child.html',
                           title='Sign In',
                           form=form)


@app.route('/create_task', methods=['GET', 'POST'])
def add_task():
    if session['id'] is not None:
        if session['status'] == 'parent':
            conn, c = connect_db()
            sql = ("SELECT id_child, login FROM children where id_parent = '{}'".format(session['id']))
            c.execute(sql)
            form = Addtaskform()
            form.childrens.choices = c.fetchall()
            print(form.data)
            if form.validate_on_submit():
                uid_parent = session['id_parent']
                create_task(uid_parent, form.childrens.data,  form.description.data, form.coin.data)
                print(1)
                return redirect('/index')
            return render_template('add_task.html',
                                   title='add_task',
                                   form=form)
    return redirect('/index')


@app.route('/view_task', methods=['GET', 'POST'])
def view_task():
    if session['id'] is not None:
        if session['status'] == 'parent':
            conn, c = connect_db()
            sql = ("SELECT children.name, children.surname, children.patronymic, tasks.description, tasks.coin,"
                   " tasks.status  FROM tasks, children where tasks.id_parent = '{}' and children.id_parent = '{}'"
                   "".format(session['id'][0], session['id'][0]))
            print(sql)
            c.execute(sql)
            result = c.fetchall()
            print(result)
            return render_template('view_task.html', title='view_task',
                                       status=session['status'], tasks=result)
        elif session['status'] == 'children':
            conn, c = connect_db()
            sql = ("SELECT * FROM tasks where id_child = '{}'".format(session['id'][0]))
            c.execute(sql)
            result = c.fetchall()

            sql = ("SELECT name, surname, patronymic FROM children where id_child = '{}'".format(session['id'][0]))
            c.execute(sql)
            resul = c.fetchall()
    #   Добавить рендеринг результата
            return render_template('view_task.html', title='view_task',
                               status=session['status'], tasks=result, fio=resul[0])
    return redirect('/index')


@app.route('/close_task', methods=['GET', 'POST'])
def close_task():
    if session['id'] is not None:
        if session['status'] == 'parent':
            conn, c = connect_db()
            sql = ("SELECT id_task, description FROM tasks where id_parent = '{}' and status = '1'".format(session['id']))
            c.execute(sql)
            #print(c.fetchall())
            form = closetaskform()
            form.tasks.choices = c.fetchall()
            print(form.data)
            if form.validate_on_submit():
                uid_parent = session['id_parent']
                create_task(uid_parent, form.childrens.data, form.description.data, form.coin.data)
                print(1)
                return redirect('/index')
            return render_template('close_task.html',
                                   title='close_task',
                                   form=form)
        elif session['status'] == 'children':
            conn, c = connect_db()
            sql = ("SELECT * FROM tasks where id_child = '{}' and status = '0'".format(session['id']))
            c.execute(sql)
            form = closetaskform()
            form.tasks.choices = c.fetchall()
            print(form.data)
            if form.validate_on_submit():
                uid_parent = session['id_parent']
                create_task(uid_parent, form.childrens.data, form.description.data, form.coin.data)
                print(1)
                return redirect('/index')
            return render_template('close_task.html',
                                   title='close_task',
                                   form=form)
    return redirect('/index')
