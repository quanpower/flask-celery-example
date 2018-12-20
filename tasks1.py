#-*-coding:utf-8-*-   

import os
import random
import time
# from flask import Flask, request, render_template, session, flash, redirect, \
#     url_for, jsonify

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from db import ProductionLine, PLCProtocol, PLCType, DBType, Device
import json
# from flask_mail import Mail, Message
from celery import Celery, chain, signature
import time


import paho.mqtt.client as mqtt    
import struct



# Initialize Celery
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)
app = Celery('tasks1', broker='redis://localhost:6379/0',backend='redis://localhost:6379/0')

connect = create_engine("mysql+pymysql://root:caojing1010@localhost:3306/damao",
                        encoding="utf-8",
                        echo=True)  # 连接数据库，echo=True =>把所有的信息都打印出来
DBSession = sessionmaker(bind=connect)
db_session = DBSession()



@app.task
def query_device_distributed(units):
    """Background task to send an email with Flask-Mail."""
    print("------in query_device_distributed task!-------")
    
    time.sleep(0.03)

    return units



@app.task
def query_device(units):
    """Background task to send an email with Flask-Mail."""
    print("------in query device task!-------")
    device_id=1
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

        return units
        # res = queryPLCType.apply_async((device.PLCType_id), link=queryPLCProtocol.s())
        # print(res.get())



@app.task
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


@app.task
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



@app.task
def queryParameter(PLCProtocol_id):
    """Background task to send an email with Flask-Mail."""
    print("----in queryParameter task!-----")

    time.sleep(0.05)
    parameters = {'x0':True}
    return parameters


@app.task
def parseParameter(parameters):
    """Background task to send an email with Flask-Mail."""
    print("----in parseParameter task!-----")

    time.sleep(0.03)
    parameters_json = json.dumps(parameters)
    return parameters_json


@app.task
def uploadMES(parameters_json):
    """Background task to send an email with Flask-Mail."""
    print("----in uploadMES task!-----")

    time.sleep(0.02)

    return 'upload succeefully!'


