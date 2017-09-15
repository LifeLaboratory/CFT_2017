from app import app
from flask import Flask, request, redirect, url_for
from flask import render_template, flash, redirect
from app.check_parents_and_children import check_login
from app.forms import LoginForm, addregexform
from app.forms import Regform, closetaskform, bonusform
from app.forms import AddchildForm, Addtaskform, requestaddform
from flask import make_response, session


from app.api.money.transaction import transaction
from app.api.money.qiwi import QIWI

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
from app.api.database.close_requests_user import close_requests_user


myqiwi=QIWI('+79069700068','3a802710e7f2e71ca559764a8a60df21' )
antqiwi=QIWI('+79137144010','94b289a122758199dac27ad2f47e9144')
@app.route('/', methods=['GET'])
@app.route('/index')

def index():
    '''
    Функция страницы index. При входе неавторизированного пользователя показывает страницу приветствия.
    При входе родителя или ребенка показываются соответствующие страницы.
    Выводится баланс счетов.
    '''
    try:
        if session['id'] is not None:
            if session['status'] == 'parent':
                balance_p = myqiwi.get_balance()["accounts"][0]["balance"]["amount"]
                conn, c = connect_db()
                sql = ("SELECT id_child, name, surname, patronymic FROM children where id_parent = '{}'".format(session['id']))
                c.execute(sql)
                balance_c = {child[1]: antqiwi.get_balance()["accounts"][0]["balance"]["amount"] for child in c.fetchall()}
                return render_template("index_parent.html",
                                       len_balance_c=len(balance_c)+2,
                                       balance_p=balance_p,
                                       balance_c=balance_c,
                                       valid = session['status'])
            elif session['status'] == 'children':
                conn, c = connect_db()
                sql = ("SELECT id_child, name, surname, patronymic FROM children where id_child = '{}'".format(session['id']))
                c.execute(sql)
                balance_c = {child[1]: antqiwi.get_balance()["accounts"][0]["balance"]["amount"] for child in c.fetchall()}
                return render_template("index_children.html",
                                    len_balance_c=len(balance_c)+1,
                                       balance_c=balance_c,
                                       valid=session['status'])
    except:
        return render_template("index.html")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    '''
    Регистрация родителя. Вводятся логин, пароль, повтор пароля, имя. фамилия, отчетство, пол и номер телефона.
    Делается запись в базе данных.
    '''
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
                                form.surname.data, form.patronymic.data, form.sex.data,
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
    '''Логин пользователя через связку логин/пароль'''
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
    '''
    Регистрация ребенка. Это может сделать родитель при входе в систему. Выбранная им связка логина пароля будет использоваться
    ребенком для входа.
    '''
    if session['id'] is not None:
        if session['status'] == 'parent':
            form = AddchildForm()
            if form.validate_on_submit():
                uid_parent = session['id']
                create_child(uid_parent, form.login.data, form.password.data, form.name.data,
                              form.surname.data, form.patronymic.data, form.sex.data, form.number_close.data)
                return redirect('/index')
            return render_template('add_child.html',
                                   title='Sign In',
                                   form=form,
                                   valid=session['status'])
    return redirect('/index')


@app.route('/create_task', methods=['GET', 'POST'])
def add_task():
    '''
    Создание задач для ребенка. Запрос в базу данных о детях связаных с родителем через id
    Вывод списка детей с полями описания задачи и ценой за выполнение.
    '''
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
    '''Просмотр задач. Если зашел родитель видит все задачи для всех своих детей.
    Если зашел ребенок, то видит только свои задачи.
    Запрос в базу данных о задачах по id пользователя'''
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
            return render_template('view_task_child.html', title='view_task',
                                   valid=session['status'], tasks=result, fio=resul[0])
    return redirect('/index')


@app.route('/close_task', methods=['GET', 'POST'])
def close_task():
    '''
    Закрыть таск может только родитель, если ребенок отметил, что это задачу он выполнил.
    В интерфейсе статус: Ожидает подтверждение выполнения родителем
    В базе данных статус: 1
    Запрос в базу данных по всем задачам со статусом 1, формирование списка.
    При выборе задания перевод денег translationQIWI
    '''
    if session['id'] is not None:
        if session['status'] == 'parent':
            conn, c = connect_db()
            sql = ("SELECT id_task, description "
                   "FROM tasks where id_parent = '{}' and status = '1'".format(session['id']))
            c.execute(sql)
            result = c.fetchall()
            form = closetaskform()
            form.tasks.choices = result
            if form.validate_on_submit():
                close_task_user(form.tasks.data, session['id'], 2)
                sql = "select id_child, coin from tasks where status = 2 and id_task = '{}'".format(form.tasks.data)
                c.execute(sql)
                result = c.fetchall()
                #transaction.bonus(result[0][1], session['id'], result[0][0])
                print(myqiwi.translationQIWI("+79069700068", "+79137144010", result[0][1], "pay_children"))
                return redirect("/view_task")
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
                return redirect('/view_task')
            return render_template('close_task.html',
                                   title='close_task',
                                   form=form,
                                   valid=session['status'])
    return redirect('/index')


@app.route('/create_regex', methods=['GET', 'POST'])
def add_regex():
    '''
    Создание нужд для ребенка.
    Запрос в базу о детях, формирование списка.
    При выборе в списке и описании заносится информация а базу данных.
    '''
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
                    return redirect('/view_regex')
                return render_template('add_regex.html',
                                       title='add_regex',
                                       form=form,
                                       valid=session['status'])
    except:
        return redirect('/index')


@app.route('/view_regex', methods=['GET', 'POST'])
def view_regex():
    '''
    Просмотр нужд ребенка.
    Запрос в базу данных о детях.
    Формирование таблицы и вывод на экран
    '''
    try:
        if session['id'] is not None:
            if session['status'] == 'parent':
                conn, c = connect_db()
                sql = ("SELECT id_child FROM children where id_parent = '{}'".format(session['id']))
                c.execute(sql)
                result_c = c.fetchall()
                ans = []
                for child in result_c:
                    print(child)
                    sql = ("SELECT id_child, description FROM regex where id_child = '{}'".format(child[0]))
                    print(sql)
                    c.execute(sql)
                    result_p = c.fetchall()
                    print(result_p)
                    for i in result_p:
                        sql = "SELECT name, surname, patronymic FROM children where id_child = '{}'".format(i[0])
                        c.execute(sql)
                        r = c.fetchall()
                        ans.append((r[0][0], r[0][1], r[0][2], i[1]))
                print(ans)
                return render_template('view_regex.html',
                                       title='add_regex',
                                       result=ans,
                                       valid=session['status'])
    except:
        return redirect('/index')



@app.route('/score', methods=['GET', 'POST'])
def add_score():
    '''Дневник школьника. Запросом в базу находит детей по id Родителя.
    Получает оценки с помощью функции average_score и формируется таблица

    Есть форма, для перевода денег ребенку, за хорошие оценки'''
    try:
        if session['id'] is not None:
            if session['status'] == 'parent':
                form = bonusform()
                conn, c = connect_db()
                sql = ("SELECT id_child, login FROM children where id_parent = '{}'".format(session['id']))
                c.execute(sql)
                #form = Addtaskform()
                form.childrens.choices = c.fetchall()
                if form.validate_on_submit():

                    #transaction.bonus(form.coin.data, session['id'], form.childrens.data)
                    print(myqiwi.translationQIWI("+79069700068", "+79137144010", form.coin.data, "pay_children"))
                    return redirect("/score")
                #conn, c = connect_db()
                sql = ("SELECT id_child, name, surname, patronymic "
                       "FROM children where id_parent = '{}'".format(session['id']))
                c.execute(sql)

                l = {child[1] + ' ' + child[2] + ' ' + child[3]:
                         average_score(child[1] + ' ' + child[2] + ' ' + child[3])
                     for child in c.fetchall()}
                print (l)

                s = 0
                ans = []
                for score in l:
                    s = 0
                    for sc in l[score]:
                        if sc != 'name' and sc != 'mean':
                            s += float(l[score][sc])
                    l[score]['mean'] = str(round(s/(len(l[score])-1), 1))
                    #ans.append(str(round(s/(len(l[score])-1), 1)))
                return render_template('score.html',
                                       title='add_score',
                                       users=l,
                                       form=form,
                                       valid=session['status'])
    except:
        return redirect('/index')


@app.route('/requests', methods=['GET', 'POST'])
def request():
    '''
    Запрос в базу данных с запросами (requests) по id родителя и статусом 0
    Статус 0 = Запрос открыт
    Статус 1 = запрос закрыт
    Формирование таблицы и вывод на экран
    '''
    try:
        if session['id'] is not None:
            if session['status'] == 'parent':
                conn, c = connect_db()
                sql = "SELECT id_child, description, coin FROM requests where id_parent = '{}' and status = 0".format(session['id'])
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
                    return redirect('/index')
                return render_template('request_child.html',
                                       title='add_task',
                                       form=form,
                                       result=result,
                                       valid=session['status'])
    except:
        return redirect('/index')


@app.route('/close_requests', methods=['GET', 'POST'])
def close_requests():
    '''
    Запрос в базу данных с запросами (requests) по id родителя и статусом 0
    Статус 0 = Запрос открыт
    Статус 1 = запрос закрыт
    Формирование списка. При нажатии кнопки перевод денег и запрос получает статус 1
    '''
    try:
        if session['id'] is not None:
            if session['status'] == 'parent':
                conn, c = connect_db()
                sql = ("SELECT id_requests, description "
                       "FROM requests where id_parent = '{}' and status = 0".format(session['id']))
                c.execute(sql)
                result = c.fetchall()
                form = closetaskform()
                form.tasks.choices = result
                if form.validate_on_submit():
                    close_requests_user(form.tasks.data)
                    sql = "select id_child, coin from requests where status = 1 and id_requests = '{}'".format(form.tasks.data)
                    c.execute(sql)
                    result = c.fetchall()
                    #$print (result[0][1], session['id'], result[0][0])
                    #transaction.bonus(result[0][1], session['id'], result[0][0])
                    print(myqiwi.translationQIWI("+79069700068", "+79137144010", result[0][1], "pay_children"))
                    return redirect("/requests")
                return render_template('close_requests.html',
                                       title='add_task',
                                       form=form,
                                       valid=session['status'])
    except:
        return redirect('/index')


@app.route('/pay_children', methods=['GET', 'POST'])
def pay_children():
    '''
    Запрос в базу о детях
    Вывод списка.
    При нажатии кнопки перевод.
    '''
    try:
        if session['id'] is not None:
            if session['status'] == 'parent':
                conn, c = connect_db()
                sql = ("SELECT id_child, login FROM children where id_parent = '{}'".format(session['id']))
                c.execute(sql)
                form = bonusform()
                form.childrens.choices = c.fetchall()
                if form.validate_on_submit():
                    #transaction.bonus(form.coin.data, session['id'], form.childrens.data)
                    print (myqiwi.translationQIWI("+79069700068", "+79137144010", form.coin.data, "pay_children"))
                    return redirect("/index")
                return render_template('pay_children.html',
                                       title='add_task',
                                       form=form,
                                       valid=session['status'])
    except:
        return redirect('/index')


@app.route('/block_pay_children', methods=['GET', 'POST'])
def block_pay_children():
    try:
        '''
        Запрос в базу о детях
        Вывод списка.
        При нажатии кнопки обратный перевод от ребенка родителю.
        '''
        if session['id'] is not None:
            if session['status'] == 'parent':
                conn, c = connect_db()
                sql = ("SELECT id_child, login FROM children where id_parent = '{}'".format(session['id']))
                c.execute(sql)
                form = bonusform()
                form.childrens.choices = c.fetchall()
                if form.validate_on_submit():
                    #transaction.mulctl(form.coin.data, session['id'], form.childrens.data)
                    print(antqiwi.translationQIWI("+79137144010", "+79069700068", form.coin.data, "pay_children"))
                    return redirect("/index")
                return render_template('block_pay_children.html',
                                       title='add_task',
                                       form=form,
                                       valid=session['status'])
    except:
        return redirect('/index')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    '''
    Выход
    '''
    session.pop('id', None)
    session.pop('status', None)
    session.pop('login', None)
    return render_template('index.html')