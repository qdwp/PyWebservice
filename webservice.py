# coding=utf-8
import cookielib
from flask import Flask, make_response, request, redirect, json
from library.login import Login
from library.handlers.courseHandler import Course
from library.handlers.taskHandler import Task
from library.handlers.makeUpHandler import MakeUp
from library.handlers.scoreHandler import Score
from library.handlers.avgPointHandler import Avg
from library.handlers.updateHandler import Update
from library.saveBaseInfo import MyThread

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def default():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    cookies = cookielib.CookieJar()
    userid = ""
    if request.method == 'POST':
        username = request.json['uid']
        password = request.json['pwd']
        if username is None or password is None:
            response = make_response(json.dumps({'success': False, "msg": '登陆失败，用户名或密码为空'}))
            return response
        cookies, userid = Login.login(username, password)
    elif request.method == 'GET':
        username = request.args.get('uid')
        password = request.args.get('pwd')
        
        if username is None or password is None:
            response = make_response(json.dumps({'success': False, "msg": '登陆失败，用户名或密码为空'}))
            return response
        cookies, userid = Login.login(username, password)

    if cookies is None:
        response = make_response(json.dumps({'success': False, "msg": '登陆失败，用户名或密码错误'}))
    else:
        response = make_response(json.dumps({'success': True, "username": userid, "userpwd": password}))
    return response


@app.route('/getCourse', methods=['GET', 'POST'])
def course():
    username = None
    password = None
    version = None
    model = None
    apk = None
    if request.method == 'POST':
        username = request.json['uid']
        password = request.json['pwd']
        version = request.json['ver']
        model = request.json['mod']
        apk = request.json['apk']
    elif request.method == 'GET':
        username = request.args.get('uid')
        password = request.args.get('pwd')
        version = request.args.get('ver')
        model = request.args.get('mod')
        apk = request.args.get('apk')
        # username = ''
        # password = ''
    try:
        cookies, userid = Login.login(username, password)
        if cookies is None:
            raise Exception("登陆失败，用户名或密码错误")

        course_url = 'http://211.70.149.135:88/xskbcx.aspx?gnmkdm=N121603&xh='
        course_url += userid
        config_data = {
            'url': course_url,
            'cookies': cookies,
            'pwd': password
        }
        _course = Course(config_data)
        student = None
        contents, student = _course.get_courses()
        if contents is None:
            raise Exception('服务器错误，无法解析课表信息')
        else:
            # print student.get('userXH')
            my_thread = MyThread(student, version, model, apk)
            my_thread.start()
            return make_response(contents)
    except Exception, ex:
        return make_response(json.dumps({'success': False, "msg": ex.message}))


@app.route('/getTaskInfo', methods=['GET', 'POST'])
def task():
    username = None
    password = None
    xnd = None
    xqd = None
    if request.method == 'POST':
        username = request.json['uid']
        password = request.json['pwd']
        xnd = request.json['xnd']
        xqd = request.json['xqd']
    elif request.method == 'GET':
        # username = request.args.get('uid')
        # password = request.args.get('pwd')
        # xnd = request.args.get('xnd')
        # xqd = request.args.get('xqd')
        username = ''
        password = ''
        xnd = '2015-2016'
        xqd = '2'
    try:
        cookies, userid = Login.login(username, password)
        if cookies is None:
            raise Exception("登陆失败，用户名或密码错误")

        test_url = 'http://211.70.149.135:88/xskscx.aspx?gnmkdm=N121604&xh='
        test_url += userid
        config_data = {
            'url': test_url,
            'cookies': cookies,
            'xnd': xnd,
            'xqd': xqd
        }
        test = Task(config_data)
        param = test.get_param()
        contents = test.get_info(param)
        if contents is None:
            raise Exception('服务器错误，无法解析考试信息')
        else:
            return make_response(contents)
    except Exception, ex:
        return make_response(json.dumps({'success': False, "msg": ex.message}))


@app.route('/getMakeUpInfo', methods=['GET', 'POST'])
def makeup():
    username = None
    password = None
    xnd = None
    xqd = None
    if request.method == 'POST':
        username = request.json['uid']
        password = request.json['pwd']
        xnd = request.json['xnd']
        xqd = request.json['xqd']
    elif request.method == 'GET':
        # username = request.args.get('uid')
        # password = request.args.get('pwd')
        # xnd = request.args.get('xnd')
        # xqd = request.args.get('xqd')
        username = ''
        password = ''
        xnd = '2014-2015'
        xqd = '1'
    try:
        cookies, userid = Login.login(username, password)
        if cookies is None:
            raise Exception("登陆失败，用户名或密码错误")

        makeup_url = 'http://211.70.149.135:88/xsbkkscx.aspx?gnmkdm=N121613&xh='
        makeup_url += userid
        config_data = {
            'url': makeup_url,
            'cookies': cookies,
            'xnd': xnd,
            'xqd': xqd
        }
        test = MakeUp(config_data)
        param = test.get_param()
        contents = test.get_info(param)
        if contents is None:
            raise Exception('服务器错误，无法解析补考信息')
        else:
            return make_response(contents)
    except Exception, ex:
        return make_response(json.dumps({'success': False, "msg": ex.message}))


@app.route('/getScore', methods=['GET', 'POST'])
def score():
    username = None
    userid = None
    drop_xn = None
    drop_xq = None
    drop_type = None
    button_cjcx = None
    hid_dqszj = None
    if request.method == 'POST':
        username = request.json['uid']
        userid = request.json['tid']
        drop_xn = request.json['drop_xn']
        drop_xq = request.json['drop_xq']
        drop_type = '全部成绩'
        button_cjcx = '查询'
        hid_dqszj = ''
    elif request.method == 'GET':
        # username = request.args.get('uid')
        # password = request.args.get('pwd')
        # drop_xn = request.args.get('drop_xn')
        # drop_xq = request.args.get('drop_xq')
        username = ''
        userid = ''
        drop_xn = ''
        drop_xq = ''
        drop_type = '全部成绩'
        button_cjcx = '查询'
        hid_dqszj = ''
    try:
        score_url = 'http://211.70.149.134:8080/stud_score/brow_stud_score.aspx'
        config_data = {
            'url': score_url,
            'userid': userid,
            'username': username,
            'drop_xn': drop_xn,
            'drop_xq': drop_xq,
            'drop_type': drop_type,
            'button_cjcx': button_cjcx,
            'hid_dqszj': hid_dqszj
        }
        test = Score(config_data)
        param = test.get_param()
        contents = test.get_info(param)
        if contents is None:
            raise Exception('服务器错误，无法解析成绩信息')
        else:
            return make_response(contents)
    except Exception, ex:
        return make_response(json.dumps({'success': False, "msg": ex.message}))


@app.route('/getAvgPoint', methods=['GET', 'POST'])
def avg():
    username = None
    userid = None
    drop_xn = None
    drop_xq = None
    drop_type = None
    button_cjcx = None
    hid_dqszj = None
    if request.method == 'POST':
        username = request.json['uid']
        # userid = request.json['tid']
    elif request.method == 'GET':
        # username = request.args.get('uid')
        # userid = request.args.get('tid')
        # username = ''
        # userid = ''
        username = ''
    userid = ''
    drop_xn = ''
    drop_xq = ''
    drop_type = '全部成绩'
    button_xfj = '第一专业平均学分绩'
    hid_dqszj = ''
    try:
        score_url = 'http://211.70.149.134:8080/stud_score/brow_stud_score.aspx'
        config_data = {
            'url': score_url,
            'userid': userid,
            'username': username,
            'drop_xn': drop_xn,
            'drop_xq': drop_xq,
            'drop_type': drop_type,
            'button_xfj': button_xfj,
            'hid_dqszj': hid_dqszj
        }
        test = Avg(config_data)
        param = test.get_param()
        contents = test.get_info(param)
        if contents is None:
            raise Exception('服务器错误，无法解析学分绩信息')
        else:
            return make_response(contents)
    except Exception, ex:
        return make_response(json.dumps({'success': False, "msg": ex.message}))


@app.route("/getUpdateInfo", methods=['GET', 'POST'])
def update():
    content = None
    if request.method == "GET":
        up = Update()
        content = up.get_version()
    elif request.method == "POST":
        version = request.json['version']
        up = Update()
        content = up.set_version(version)
    if content is not None:
        return make_response(json.dumps({'success': True, 'update': content}))
    else:
        return make_response(json.dumps({'success': False, 'msg': '检查更新文件失败'}))


@app.errorhandler(400)
def not_found(error):
    return make_response(json.dumps({'success': False, "msg": '400 BAD REQUEST'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps({'success': False, "msg": '404 NOT FOUND'}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(json.dumps({'success': False, "msg": '405 METHOD NOT ALLOWED'}), 405)


@app.errorhandler(500)
def not_found(error):
    return make_response(json.dumps({'success': False, "msg": '500 INTERNAL SERVER ERROR'}), 500)


if __name__ == '__main__':
    app.run()
