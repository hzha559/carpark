import asyncio
import time
#from quart import Quart, render_template, websocket
from flask import Flask, request, flash, render_template, redirect, url_for, jsonify
from flask_login import UserMixin, LoginManager, login_required, logout_user, login_user, current_user
import logging
from flask import Response
import pymssql
from waitress import serve
from threading import Thread
# 创建 Flask 应用
app = Flask(__name__)
#app = Quart(__name__)

app.secret_key = 'secret_key'  # 设置表单交互密钥



example={
    "firstName":"xiaochuan",
    "lastName":"sun",
    "email":"123@hotmail.com",
    "appointmentTime":"2022-03-01 19:00"
}



# 模拟数据库查询
class UserService:
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

def queryall():
    conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
    cur = conn.cursor()
    query = 'SELECT * FROM [1].[dbo].[appointment] '
    # query += 'where month=\'2022-02\' and assetid like \'%-EM-%\''
    # query = query.replace('-EM-', meter)
    # query = query.replace('2022-02', month)
    try:
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
        user = {'vav': result2}
    except Exception as e:
        result2 = {'key': e, 'data': e}
        user={'vav': result2}
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
def change():
    if request.method == 'POST':
        if request.json['id'][0:4]=='dele':
            conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
            cur = conn.cursor()
            query = 'delete from Appointment '
            query += 'where trendkey=125'
            query = query.replace('125', request.json['id'][4:])
            try:
                cur.execute(query)
            except Exception as e:
                logging.warning(e)
            conn.commit()
            return jsonify(queryall())
        elif request.json['id'][0:4]=='save':
            conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
            cur = conn.cursor()
            rego=request.json['rego']
            data=request.json['data']

            query='update Appointment set[rego] = \'1pv3oh\''
            query+='where email = \'123@hotmail.com\' and convert(nvarchar(MAX), datetime, 120) = \'2022-03-01\''
            query=query.replace('1pv3oh',rego)
            query = query.replace('123@hotmail.com',data[3])
            query = query.replace('2022-03-01', data[5])
            try:
                cur.execute(query)
            except Exception as e:
                logging.warning(e)
            conn.commit()
            return jsonify(queryall())
    return 1

def post_to_carpark():
    from math import factorial
    time.sleep(100)
    print('posted to carpark')
    return 0

@app.route('/pms', methods=['GET', 'POST'])
def receive_post():
    if request.method == 'POST':
        logging.warning(request.json['firstName'])
        conn = pymssql.connect(host='127.0.0.1', user='sa', password='12345678', database='1')
        cur = conn.cursor()
        query='insert into Appointment values'
        query+='(\'wang\', \'jie\', \'2@qq.com\', \'\', \'2022-04-01 03:00\', \'2022-06-22 00:00\')'
        query=query.replace('wang',request.json['firstName'])
        query=query.replace('jie', request.json['lastName'])
        query=query.replace('2@qq.com', request.json['email'])
        query=query.replace('2022-04-01 03:00', request.json['appointmentTime'])
        #query.replace('2022-06-22 00:00', request.json['updatetime'])
        try:
            cur.execute(query)
        except Exception as e:
            logging.warning(e)
        conn.commit()
        Thread(target = post_to_carpark).start()
        return '200'
    else:
        return '401'

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
            logging.warning('here')
            curr_user = User()
            curr_user.id = user['id']

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)

            # 登录成功后重定向
            next_url = request.args.get('next')
            return redirect(next_url or url_for('index'))

        return ('Wrong username or password!')

    else:
        # GET 请求
        return render_template('login.html')


# 5、登出功能实现
@app.route('/logout')
@login_required
def logout():
    # 通过Flask-Login的logout_user方法登出用户
    logout_user()
    return 'Logged out successfully!'

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
    result2={'key':trendkey,'data':result1}
    user= {'vav':result2}
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
    user = {'vav': result2}
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

@app.route('/delta',methods=['POST','GET'])
def delta():
    result1=[[3, 'leo', 401001001, '1st3tt', '2022-04-01 07:00:00', '2022-03-01 00:00:00']]
    user = {'vav': result1}

    return jsonify(user)

if __name__ == '__main__':
    #serve(app, host='0.0.0.0', port=2556)
    app.run(host='0.0.0.0', port=2556,threaded=True)
