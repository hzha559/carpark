import asyncio
import time
#from quart import Quart, render_template, websocket
from datetime import timedelta

from flask import Flask, request, flash, render_template, redirect, url_for, jsonify,session
from flask_login import UserMixin, LoginManager, login_required, logout_user, login_user, current_user
import logging
from flask import Response
import pymssql
from waitress import serve
from threading import Thread
from os.path import exists
# 创建 Flask 应用
app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(hours=5)

app.secret_key = 'secret_key'  # 设置表单交互密钥



example={
    "firstName":"xiaochuan",
    "lastName":"sun",
    "email":"123@hotmail.com",
    "appointmentTime":"2022-03-01 19:00"
}



# 模拟数据库查询
class UserService:
    conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
    cur = conn.cursor()
    query = 'SELECT * FROM [1].[dbo].[user] '
    # query += 'where month=\'2022-02\' and assetid like \'%-EM-%\''
    # query = query.replace('-EM-', meter)
    # query = query.replace('2022-02', month)
    cur.execute(query)
    result=cur.fetchall()
    users=[]
    #for item in result:
        #users.append(item)

    users = [
        {'id': 1, 'username': 'tom', 'password': '1'},
        {'id': 2, 'username': 'jack', 'password': '2'}
    ]

    @classmethod
    def query_user_by_name(cls, username):
        for user in cls.users:
            if username == user['username']:
                return user

    @classmethod
    def query_user_by_id(cls, user_id):
        for user in cls.users:
            if user_id == user['id']:
                return user




def updatedel(statement,filter):
    conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
    cur = conn.cursor()
    query = statement+filter
    try:
        #logging.warning(query)
        cur.execute(query)
        conn.commit()
        return 0
    except Exception as e:
        return e



def queryall(filter):
    conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
    cur = conn.cursor()
    commit=0
    if  filter[0:6]=='insert':
        #logging.warning(filter)
        query=filter
        commit=1
    else:
        query = 'SELECT * FROM [1].[dbo].[appointment] '
        query+=filter
    logging.warning(query)
    try:

            cur.execute(query)
            if commit==1:
                conn.commit()
                return 0
            else:
                result = cur.fetchall()
                result1 = []
                trendkey = []
                for i in range(len(result)):
                    result1.append([])
                    trendkey.append([])
                    trendkey[i].append(result[i][0])
                    result1[i].append(result[i][0])
                    result1[i].append(result[i][1])
                    result1[i].append(result[i][2])
                    result1[i].append(result[i][3])
                    result1[i].append(str(result[i][4]))
                    result1[i].append(str(result[i][5]))
                    result1[i].append(str(result[i][6]))
                # logging.warning(result1)
                result2 = {'key': trendkey, 'data': result1}
                user = {'vav': result2,'submit':0}
    except Exception as e:
            result2 = {'key': e, 'data': e}
            user={'vav': result2,'submit':0}
    return user

# 1、实例化登录管理对象
login_manager = LoginManager()

# 参数配置
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'

login_manager.init_app(app)  # 初始化应用


# 2、编写用户类
class User(UserMixin):
    pass

@app.route('/delta', methods=['GET', 'POST'])
#used for admin
@login_required
def change():
    #logging.warning(request.json['id']=='add')
    #logging.warning(request.json['tempall'])

    if request.method == 'POST':
        if request.json['id'][0:4]=='dele':
            query = 'delete from Appointment '
            query1 = 'where trendkey=125'
            query1 = query1.replace('125', request.json['id'][4:])
            updatedel(query,query1)
            result = queryall('')
            Thread(target=post_to_carpark, args=(result,)).start()
            return jsonify(result)
        elif request.json['id']=='add':
            firstname=request.json['tempall'][1]
            lastname=request.json['tempall'][2]
            email=request.json['tempall'][3]
            rego=request.json['tempall'][4]
            appointmentdate=request.json['tempall'][5]
            updatedtime=request.json['tempall'][6]
            query='insert into[1].[dbo].[Appointment] values '
            query+='(\'namea\', \'nameb\', \'1@qq.com\', \'rego1234\', \'2022-05-01a\', \'2022-06-01b\')'
            query=query.replace('namea',firstname)
            query = query.replace('nameb', lastname)
            query = query.replace('1@qq.com', email)
            query = query.replace('rego1234', rego)
            query = query.replace('2022-05-01a', appointmentdate)
            query = query.replace('2022-06-01b', updatedtime)
            queryall(query)
            result=queryall('')
            logging.warning(result)
            return jsonify(result)



        elif request.json['id'][0:4]=='save':
            rego=request.json['rego']
            data=request.json['data']
            query='update Appointment set[rego] = \'1pv3oh\''
            query1='where email = \'123@hotmail.com\' and convert(nvarchar(MAX), datetime, 120) = \'2022-03-01\''
            query=query.replace('1pv3oh',rego)
            query1 = query1.replace('123@hotmail.com',data[3])
            query1 = query1.replace('2022-03-01', data[5])

            updatedel(query,query1)
            result=queryall('')
            time.sleep(5)
            #logging.warning(result['submit'])
            #Thread(target=post_to_carpark, args=(result,)).start()
            return jsonify(result)

        else:
            return jsonify(queryall(''))
    return 1

@app.route('/deltaclient', methods=['GET', 'POST'])
def change1():
    if request.method == 'POST':
        logging.warning(request.json['id'])
        if request.json['id'][0:4]=='sear':
            email=request.json['email']
            date=request.json['date']
            #logging.warning(email,date)
            #query='select * from Appointment '
            query=' where email = \'123@hotmail.com\' and left(convert(nvarchar(MAX), datetime, 120),10) = \'2022-03-01\''

            query = query.replace('123@hotmail.com',email)
            query = query.replace('2022-03-01', date)
            #updatedel(query)
            return jsonify(queryall(query))
        elif request.json['id']=='update':
            email = request.json['email']
            date = request.json['date']
            rego=request.json['rego']
            # logging.warning(email,date)
            # query='select * from Appointment '
            query = 'update Appointment set[rego] = \'1pv3oh\''
            query1= ' where email = \'123@hotmail.com\' and left(convert(nvarchar(MAX), datetime, 120),10) = \'2022-03-01\''
            query = query.replace('1pv3oh', rego)
            query1 = query1.replace('123@hotmail.com', email)
            query1 = query1.replace('2022-03-01', date)
            #logging.warning(query)
            updatedel(query,query1)
            return jsonify(queryall(query1))
        else:
            return jsonify(' ')
            # logging.warning(queryall(query))

    return '1'

@app.route('/delta1', methods=['GET', 'POST'])
def post_to_carpark():
    result = queryall('')
    result['submit']=1
    time.sleep(10)
    print('exist ',exists('1.csv'))

    print('posted to carpark ',result['submit'])
    return jsonify(result)

@app.route('/pms', methods=['GET', 'POST'])
def receive_post():
    print(request.json)
    if request.method == 'POST':
        try:
            logging.warning(request.json['firstName'])
            conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
            cur = conn.cursor()
            query='insert into Appointment1 values'
            query+='(\'wang\', \'jie\', \'2@qq.com\', \'\', \'2022-04-01 03:00\', \'2022-06-22 00:00\')'
            query=query.replace('wang',request.json['firstName'])
            query=query.replace('jie', request.json['lastName'])
            query=query.replace('2@qq.com', request.json['email'])
            query=query.replace('2022-04-01 03:00', request.json['appointmentTime'])
            query = query.replace('2022-06-22 00:00', request.json['endTime'])
            #query.replace('2022-06-22 00:00', request.json['updatetime'])
            cur.execute(query)
        except Exception as e:
            return Response('Error: contact OI for the following error message '+str(e), status=400, mimetype='application/json')
        conn.commit()
        #Thread(target = post_to_carpark).start()
        return Response('Appointment Received', status=200, mimetype='application/json')
    else:
        return Response('Method Not Understood', status=400, mimetype='application/json')

# 3、加载用户, login_required 需要查询用户信息
@login_manager.user_loader
def user_loader(user_id: str):
    """
    [注意] 这里的user_id类型是str
    :param user_id:
    :return:
    """
    if UserService.query_user_by_id(int(user_id)) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user


# 4、登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        user = UserService.query_user_by_name(username)

        if user is not None and request.form['password'] == user['password']:
            #logging.warning('here')
            curr_user = User()
            curr_user.id = user['id']

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)
            session.permanent = True
            # 登录成功后重定向
            next_url = request.args.get('next')
            return redirect(next_url or url_for('index'))
        logging.warning('here')
        return render_template('login.html',message='Wrong Credential')

    else:
        # GET 请求
        return render_template('login.html',message='')


# 5、登出功能实现
@app.route('/logout')
@login_required
def logout():
    # 通过Flask-Login的logout_user方法登出用户
    logout_user()
    return 'Logged out successfully!'

#for patient
@app.route('/')
def index1():
    conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
    cur = conn.cursor()
    query = 'SELECT * FROM [1].[dbo].[appointment] '
    #query += 'where month=\'2022-02\' and assetid like \'%-EM-%\''
    #query = query.replace('-EM-', meter)
    #query = query.replace('2022-02', month)
    cur.execute(query)
    result = cur.fetchall()
    result1=[]
    trendkey=[]
    for i in range(len(result)):
        result1.append([])
        trendkey.append([])
        trendkey[i].append(result[i][0])
        result1[i].append(result[i][1])
        result1[i].append(result[i][2])
        result1[i].append(result[i][3])
        result1[i].append(str(result[i][4]))
        result1[i].append(str(result[i][5]))
    #logging.warning(result1)
    result2={'key':'','data':''}
    user= {'vav':result2,'submitted':1}
    response = Response(render_template("visitor.html",
                                        title='Home',
                                        user=user))
    return response


# 6、访问控制
@app.route('/admin')
@login_required
def index():
    conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
    cur = conn.cursor()
    query = 'SELECT * FROM [1].[dbo].[appointment] '
    # query += 'where month=\'2022-02\' and assetid like \'%-EM-%\''
    # query = query.replace('-EM-', meter)
    # query = query.replace('2022-02', month)
    cur.execute(query)
    result = cur.fetchall()
    result1 = []
    trendkey = []
    for i in range(len(result)):
        result1.append([])
        trendkey.append([])
        trendkey[i].append(result[i][0])
        result1[i].append(result[i][0])
        result1[i].append(result[i][1])
        result1[i].append(result[i][2])
        result1[i].append(result[i][3])
        result1[i].append(str(result[i][4]))
        result1[i].append(str(result[i][5]))
        result1[i].append(str(result[i][6]))
    # logging.warning(result1)
    result2 = {'key': trendkey, 'data': result1}
    user = {'vav': result2,'submitted':1}
    response = Response(render_template("blank.html",
                                        title='Home',
                                        user=user))
    return response

@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/notfound')
def notfound():
    return render_template('404.html')



if __name__ == '__main__':
    #serve(app, host='0.0.0.0', port=2556)
    app.run(host='0.0.0.0', port=2556,threaded=True)
