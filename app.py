import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from db import ProductionLine, PLCProtocol, PLCType, DBType, Device
import json
from flask_mail import Mail, Message
from celery import Celery, chain, signature
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = '252527676@qq.com'
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = 'picuyfuvuzgfbhig'
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = '252527676@qq.com'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# Initialize extensions
mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


connect = create_engine("mysql+pymysql://root:caojing1010@localhost:3306/damao",
                        encoding="utf-8",
                        echo=True)  # 连接数据库，echo=True =>把所有的信息都打印出来
DBSession = sessionmaker(bind=connect)
db_session = DBSession()



@celery.task
def query_device(device_id):
    """Background task to send an email with Flask-Mail."""
    print("------in query device task!-------")
    device = db_session.query(Device).filter_by(id=device_id).first()
    #打印实例
    print(device)
    print(device.id, device.isPLC)
    # isPLC?
    if device.isPLC:
        print(device.PLCType_id, device.plc_ip, device.PLC_type.name)

        # plcProtocol = queryProtocol.delay(device.PLCType_id)
        work_flow = chain(queryPLCType.s(device.PLCType_id), queryPLCProtocol.s(), queryParameter.s(), parseParameter.s(), uploadMES.s() )
        work_flow()
        print('ok')

        return 'loop over!'
        # res = queryPLCType.apply_async((device.PLCType_id), link=queryPLCProtocol.s())
        # print(res.get())






@celery.task
def queryPLCType(PLCType_id):
    """Background task to send an email with Flask-Mail."""
    print("----in queryPLCType task!-----")
    plcType = db_session.query(PLCType).filter_by(id=PLCType_id).first()
    #打印实例
    print("---plcType:----", plcType)
    print(plcType.id)
    print(plcType.PLCProtocol_id)

    time.sleep(0.02)

    return plcType.PLCProtocol_id


@celery.task
def queryPLCProtocol(PLCProtocol_id):
    """Background task to send an email with Flask-Mail."""
    print("----in queryPLCProtocol task!-----")
    plcProtocol = db_session.query(PLCProtocol).filter_by(id=PLCProtocol_id).first()
    #打印实例
    print("---PLCProtocol:----", plcProtocol)
    print(plcProtocol.id)
    print(plcProtocol.name)
    time.sleep(0.03)

    return plcProtocol.id



@celery.task
def queryParameter(PLCProtocol_id):
    """Background task to send an email with Flask-Mail."""
    print("----in queryParameter task!-----")

    time.sleep(0.05)
    parameters = {'x0':True}
    return parameters


@celery.task
def parseParameter(parameters):
    """Background task to send an email with Flask-Mail."""
    print("----in parseParameter task!-----")

    time.sleep(0.03)
    parameters_json = json.dumps(parameters)
    return parameters_json


@celery.task
def uploadMES(parameters_json):
    """Background task to send an email with Flask-Mail."""
    print("----in uploadMES task!-----")

    time.sleep(0.02)

    return 'upload succeefully!'



@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    with app.app_context():
        mail.send(msg)


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', device_id=session.get('device_id', ''))
    device_id = request.form['device_id']
    print("device_id:", device_id)
    session['device_id'] = device_id

    # # send the email
    # msg = Message('Hello from Flask',
    #               recipients=[request.form['email']])
    # msg.body = 'This is a test email sent from a background Celery task.'
    # print(msg.body)

    if request.form['submit'] == 'Send':
        # send right away
        # send_async_email.delay(msg)
        print("ready to query!")
        for i in range(1):
            # query_device.apply_async(args=[int(device_id)])
            query_device.delay(int(device_id))
            time.sleep(1)
        flash('Quering device {0}'.format(device_id))
    else:
        # send in one minute
        send_async_email.apply_async(args=[msg], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
