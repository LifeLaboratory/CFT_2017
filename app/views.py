from app import app
from flask import Flask, request, redirect, url_for
from flask import render_template, flash, redirect
from app.check_parents_and_children import check_login
from app.forms import LoginForm, addregexform
from app.forms import Regform, closetaskform
from app.forms import AddchildForm, Addtaskform, requestaddform
from flask import make_response, session


from app.api.money.transaction import transaction
# for other os0
from app.api.database.connect_db import connect_db
from app.api.database.create_parent import create_parent
from app.api.database.create_task import create_task
from app.api.database.create_children import create_child
from app.api.database.login_manager import login_in
from app.api.database.create_regex import create_regex
from app.api.database.get_balance import balance_parent, balance_child
from app.api.database.get_score_childrens import average_score
from app.api.database.create_requests import create_requests
from app.api.database.close_task import close_task_user
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
    try:
        if session['id'] is not None:
            if session['status'] == 'parent':
                balance_p = balance_parent(session['id'])
                conn, c = connect_db()
                sql = ("SELECT id_child, name, surname, patronymic FROM children where id_parent = '{}'".format(session['id']))
                c.execute(sql)
                balance_c = {child[1]+' '+child[2]+' '+child[3]: balance_child(child[0]) for child in c.fetchall()}
                return render_template("index_parent.html",
                                       len_balance_c=len(balance_c)+2,
                                       balance_p=balance_p,
                                       balance_c=balance_c,
                                       valid = session['status'])
            elif session['status'] == 'children':
                conn, c = connect_db()
                sql = ("SELECT id_child, name, surname, patronymic FROM children where id_child = '{}'".format(session['id']))
                c.execute(sql)
                balance_c = {child[1]+' '+child[2]+' '+child[3]: balance_child(child[0]) for child in c.fetchall()}
                return render_template("index_children.html",
                                    len_balance_c=len(balance_c)+2,
                                       balance_c=balance_c,
                                       valid=session['status'])
    except:
        return render_template("index.html")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        if session['id'] is None:
            return redirect('/index')
    except:
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
        try:
            if data['id'] == "Error":
                return "Wrong password or login"
        finally:
            session['login'] = form.login.data
            session['id'] = data['id'][0]
            session['status'] = data['status']
            return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/add_child', methods=['GET', 'POST'])
def add_child():
    if session['id'] is not None:
        if session['status'] == 'parent':
            form = AddchildForm()
            if form.validate_on_submit():
                uid_parent = session['id']
                create_child(uid_parent, form.login.data, form.password.data, form.name.data,
                              form.surname.data, form.patronymic.data, form.sex.data, form.number_close.data,
                              form.number_open.data, form.number_needs.data)
                return redirect('/index')
            return render_template('add_child.html',
                                   title='Sign In',
                                   form=form,
                                   valid=session['status'])
    return redirect('/index')


@app.route('/create_task', methods=['GET', 'POST'])
def add_task():
    if session['id'] is not None:
        if session['status'] == 'parent':
            conn, c = connect_db()
            sql = ("SELECT id_child, login FROM children where id_parent = '{}'".format(session['id']))
            c.execute(sql)
            form = Addtaskform()
            form.childrens.choices = c.fetchall()
            if form.validate_on_submit():
                uid_parent = session['id']
                create_task(form.childrens.data, uid_parent, form.description.data, form.coin.data)
                return redirect('/view_task')
            return render_template('add_task.html',
                                   title='add_task',
                                   form=form,
                                   valid=session['status'])
    return redirect('/index')


@app.route('/view_task', methods=['GET', 'POST'])
def view_task():
    if session['id'] is not None:
        if session['status'] == 'parent':
            print(session["id"])
            conn, c = connect_db()
            sql = "SELECT tasks.id_child, tasks.description, tasks.coin, tasks.status " \
                  "FROM tasks where tasks.id_parent = '{}' order by tasks.status".format(session['id'])
            """sql = ("SELECT children.name, children.surname, children.patronymic, tasks.description, tasks.coin,"
                   " tasks.status FROM tasks, children where tasks.id_parent = '{}' and children.id_parent = '{}'"
                   " and tasks.id_parent = children.id_parent"
                   "".format(session['id'], session['id']))"""
            c.execute(sql)
            result = c.fetchall()
            ans = []
            for i in result:
                sql = "SELECT name, surname, patronymic FROM children where id_child = '{}'".format(i[0])
                c.execute(sql)
                r = c.fetchall()
                ans.append((r[0][0], r[0][1], r[0][2], i[1], i[2], i[3]))
            return render_template('view_task_parent.html', title='view_task',
                                        valid=session['status'],
                                        tasksp=ans)
        elif session['status'] == 'children':
            conn, c = connect_db()
            sql = ("SELECT * FROM tasks where id_child = '{}' and status = 0".format(session['id']))
            c.execute(sql)
            result = c.fetchall()
            sql = ("SELECT name, surname, patronymic FROM children where id_child = '{}'".format(session['id']))
            c.execute(sql)
            resul = c.fetchall()
    #   Добавить рендеринг результата
            return render_template('view_task_child.html', title='view_task',
                                   valid=session['status'], tasks=result, fio=resul[0])
    return redirect('/index')


@app.route('/close_task', methods=['GET', 'POST'])
def close_task():
    if session['id'] is not None:
        if session['status'] == 'parent':
            conn, c = connect_db()
            sql = ("SELECT id_task, description "
                   "FROM tasks where id_parent = '{}' and status = '1'".format(session['id']))
            c.execute(sql)
            result = c.fetchall()
            print(result)
            form = closetaskform()
            form.tasks.choices = result
            if form.validate_on_submit():
                close_task_user(form.tasks.data, session['id'], 2)
                sql = "select id_child, coin from tasks where status = 2 and id_task = '{}'".format(form.tasks.data)
                c.execute(sql)
                result = c.fetchall()
                print(result[0][1], ' ', result[0][0])
                transaction.in_close_to_open(result[0][1], result[0][0])
            return render_template('close_task.html',
                                   title='close_task',
                                   form=form,
                                   valid=session['status'])
        elif session['status'] == 'children':
            conn, c = connect_db()
            sql = ("SELECT id_task, description "
                   "FROM tasks where id_child = '{}' and status = '0'".format(session['id']))
            c.execute(sql)
            result = c.fetchall()
            form = closetaskform()
            form.tasks.choices = result
            if form.validate_on_submit():
                print(form.tasks.data)
                close_task_user(form.tasks.data, session['id'], 1)
                #return redirect('/index')
            return render_template('close_task.html',
                                   title='close_task',
                                   form=form,
                                   valid=session['status'])
    return redirect('/index')


@app.route('/create_regex', methods=['GET', 'POST'])
def add_regex():
    try:
        if session['id'] is not None:
            if session['status'] == 'parent':
                conn, c = connect_db()
                sql = ("SELECT id_child, login FROM children where id_parent = '{}'".format(session['id']))
                c.execute(sql)
                form = addregexform()
                form.childrens.choices = c.fetchall()
                if form.validate_on_submit():
                    create_regex(form.childrens.data,  form.description.data)
                    return redirect('/index')
                return render_template('add_regex.html',
                                       title='add_regex',
                                       form=form,
                                       valid=session['status'])
    except:
        return redirect('/index')


@app.route('/score', methods=['GET', 'POST'])
def add_score():
    try:
        if session['id'] is not None:
            if session['status'] == 'parent':
                conn, c = connect_db()
                sql = ("SELECT id_child, name, surname, patronymic "
                       "FROM children where id_parent = '{}'".format(session['id']))
                c.execute(sql)

                l = {child[1] + ' ' + child[2] + ' ' + child[3]:
                         average_score(child[1] + ' ' + child[2] + ' ' + child[3])
                     for child in c.fetchall()}
                s = 0
                ans = []
                for score in l:
                    s = 0
                    for sc in l[score]:
                        if sc != 'name':
                            s += float(l[score][sc])
                    ans.append(str(round(s/(len(l[score])-1), 1)))
                return render_template('score.html',
                                       title='add_regex',
                                       users=l,
                                       score=ans,
                                       valid=session['status'])
    except:
        return redirect('/index')


@app.route('/requests', methods=['GET', 'POST'])
def request():
#try:
    if session['id'] is not None:
        if session['status'] == 'parent':
            conn, c = connect_db()
            sql = "SELECT id_child, description, coin FROM requests where id_parent = '{}'".format(session['id'])
            c.execute(sql)
            result = c.fetchall()
            ans = []
            for i in result:
                sql = "SELECT name, surname, patronymic FROM children where id_child = '{}'".format(i[0])
                c.execute(sql)
                r = c.fetchall()
                ans.append((r[0][0], r[0][1], r[0][2], i[1], i[2]))
            return render_template('request_parent.html',
                                   title='add_task',
                                   result=ans,
                                   valid=session['status'])
        elif session['status'] == 'children':
            form = requestaddform()
            conn, c = connect_db()
            sql = "SELECT description, coin FROM requests where id_child = '{}'".format(session['id'])
            c.execute(sql)
            result = c.fetchall()
            if form.validate_on_submit():
                uid_parent = session['id']
                create_requests(uid_parent, form.description.data, form.coin.data)
            return render_template('request_child.html',
                                   title='add_task',
                                   form=form,
                                   result=result,
                                   valid=session['status'])
    #except:
     #   return redirect('/index')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('id', None)
    session.pop('status', None)
    session.pop('login', None)
    return render_template('index.html')