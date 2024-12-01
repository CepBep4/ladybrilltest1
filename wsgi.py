from flask import Flask, render_template, make_response, url_for, request, session
import json
from database import check_auth
import database
from constructer_effect import ConstructProgect
import os
from random import randint
import base64
import io
from PIL import Image
import os
#Создание приложения и уникальной подписи
app = Flask(__name__)
app.config['SECRET_KEY']='734bc427f6301f5effe583435dc1145e4cedb694'


stacs_req={}

#Страница авторизации
@app.route('/')
def login_page():
    if 'user' in session:
        if session['user']=='success':
            return render_template('home.html')
        elif session['user']=='fail': return 'False'
            #return render_template('nologincorrect.html')
    else:
        return render_template('index.html')

#Обработка попытки войти
@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        #Приём данных
        data=json.loads(request.data.decode(encoding='utf-8'))
        login=data['login']
        password=data['password']

        #Обработка данных
        check=check_auth(login=login, password=password)
        if check:
            session['user']='success'
            session['user_id']=check
            database.add(session['user_id'])
            return render_template('home.html')
        else:
            #session['user']='fail'
            return 'False'

#Уведомление для пользователей телефонов
@app.route('/phoneblock')
def phoneblock():
    return render_template('phoneblock.html')

#Обработка попытки выйти
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return render_template('index.html')

#Получение данных из куки
@app.route('/getcoockie', methods=['GET'])
def getcoockie():
    usercell=database.get(session['user_id'])
    pathList=[x.replace('.ttf','') for x in os.listdir('fonts')]
    pathList.append('Использовать свой')
    usercell['fontslist']=pathList
    return usercell

#Запись данных в куки
@app.route('/setcoockie', methods=['POST'])
def setcoockie():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])

    for params in data:
        if params=='delete':
            constructor=ConstructProgect(mode=True).load(session['user_id'])
            constructor.DeleteEffect(int(data['id']))
            constructor.GetFullLayout(session['user_id'])
            usercell['element']=constructor.lays
            constructor.save(session['user_id'])
        else:
            usercell[params]=data[params]
        if params=='select':
            #print(data)
            usercell['focus']=data['select']

    database.save(session['user_id'],usercell)
    return 'True'

#Получение айди фотоподложки
@app.route('/getlayout', methods=['POST'])
def getlayout():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    

    if session['user_id']:
        constructor=ConstructProgect(
            int(data['project_width']),
            int(data['project_height']),
            str(session['user_id'])
        )
        usercell['project_width']=str(data['project_width'])
        usercell['project_height']=str(data['project_height'])
        constructor.save(str(session['user_id']))
        usercell['element']=constructor.lays
        database.save(session['user_id'],usercell)
    return 'True'

@app.route('/addshrift', methods=['POST'])
def addshrift():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    constructor=ConstructProgect(mode=True).load(session['user_id'])

    constructor.AppendObjectText()
    constructor.GetFullLayout(session['user_id'])
    usercell['element']=constructor.lays

    if 'focus' in usercell:
        usercell['focus']=str(len(constructor.lays)-1)
    else:
        usercell['focus']=1

    constructor.save(session['user_id'])
    database.save(session['user_id'],usercell)
    return 'True'

@app.route('/editshrift', methods=['POST'])
def editshrift():
    data=json.loads(request.data.decode(encoding='utf-8'))
    if 'back' in list(data):
        usercell=database.get(session['user_id'])
        constructor=ConstructProgect(mode=True).load(session['user_id'], back_id=True)
        constructor.GetFullLayout(session['user_id'])
        usercell['focus']=data['focus']
        constructor.save(session['user_id'])
        database.save(session['user_id'],usercell)
        return 'True'
    else:
        usercell=database.get(session['user_id'])
        constructor=ConstructProgect(mode=True).load(session['user_id'])

    usercell['element'][str(data['focus'])]['params']=data['params']
    constructor.lays=usercell['element']
    usercell['focus']=data['focus']
    constructor.EditObjects(index=data['index'], effect=data['effect'], params=data['params'])
    constructor.GetFullLayout(session['user_id'])
    usercell['element']=constructor.lays

    constructor.save(session['user_id'])
    database.save(session['user_id'],usercell)
    return 'True'

@app.route('/adddot', methods=['POST'])
def adddot():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    constructor=ConstructProgect(mode=True).load(session['user_id'])

    constructor.AppendObjectDot(data['file'])
    constructor.GetFullLayout(session['user_id'])
    usercell['element']=constructor.lays

    if 'focus' in usercell:
        usercell['focus']=str(len(constructor.lays)-1)
    else:
        usercell['focus']=1

    constructor.save(session['user_id'])
    database.save(session['user_id'],usercell)
    return 'True'

@app.route('/adddotcolor', methods=['POST'])
def adddotcolor():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    constructor=ConstructProgect(mode=True).load(session['user_id'])

    constructor.AppendObjectDotColor(data['file'])
    constructor.GetFullLayout(session['user_id'])
    usercell['element']=constructor.lays

    if 'focus' in usercell:
        usercell['focus']=str(len(constructor.lays)-1)
    else:
        usercell['focus']=1

    constructor.save(session['user_id'])
    database.save(session['user_id'],usercell)
    return 'True'

@app.route('/adddotcolordia', methods=['POST'])
def adddotcolordia():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    constructor=ConstructProgect(mode=True).load(session['user_id'])

    constructor.AppendObjectDotColorDia(data['file'])
    constructor.GetFullLayout(session['user_id'])
    usercell['element']=constructor.lays

    if 'focus' in usercell:
        usercell['focus']=str(len(constructor.lays)-1)
    else:
        usercell['focus']=1

    constructor.save(session['user_id'])
    database.save(session['user_id'],usercell)
    return 'True'

@app.route('/editphoto', methods=['POST'])
def editphoto():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    constructor=ConstructProgect(mode=True).load(session['user_id'])
    data['params']['image']=usercell['element'][str(data['focus'])]['photo']

    usercell['element'][str(data['focus'])]['params']=data['params']
    constructor.lays=usercell['element']
    usercell['focus']=data['focus']
    constructor.EditObjects(index=data['index'], effect=data['effect'], params=data['params'])
    constructor.GetFullLayout(session['user_id'])
    usercell['element']=constructor.lays

    constructor.save(session['user_id'])
    database.save(session['user_id'],usercell)
    return 'True'

@app.route('/editphotocolor', methods=['POST'])
def editphotocolor():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    constructor=ConstructProgect(mode=True).load(session['user_id'])
    data['params']['image']=usercell['element'][str(data['focus'])]['photo']

    usercell['element'][str(data['focus'])]['params']=data['params']
    constructor.lays=usercell['element']
    usercell['focus']=data['focus']
    constructor.EditObjects(index=data['index'], effect=data['effect'], params=data['params'])
    constructor.GetFullLayout(session['user_id'])
    usercell['element']=constructor.lays

    constructor.save(session['user_id'])
    database.save(session['user_id'],usercell)
    return 'True'

@app.route('/editphotocolordia', methods=['POST'])
def editphotocolordia():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    constructor=ConstructProgect(mode=True).load(session['user_id'])
    data['params']['path']=usercell['element'][str(data['focus'])]['photo']

    usercell['element'][str(data['focus'])]['params']=data['params']
    constructor.lays=usercell['element']
    usercell['focus']=data['focus']
    constructor.EditObjects(index=data['index'], effect=data['effect'], params=data['params'])
    constructor.GetFullLayout(session['user_id'])
    usercell['element']=constructor.lays

    constructor.save(session['user_id'])
    database.save(session['user_id'],usercell)
    return 'True'

@app.route('/render', methods=['POST'])
def render():
    data=json.loads(request.data.decode(encoding='utf-8'))
    constructor=ConstructProgect(mode=True).load(session['user_id'])
    return constructor.RenderProject(session['user_id'], data['mirror'])

app.run(host='0.0.0.0', debug=True, port=8000) 