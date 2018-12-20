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

from tasks1 import query_device_distributed, query_device



# 当连接上服务器后回调此函数    
def on_connect(client, userdata, flags, rc):    
    print("Connected with result code "+str(rc))    
    
    # 放在on_connect函数里意味着    
    # 重新连接时订阅主题将会被更新    
    client.subscribe("0001/data")    
    

# 从服务器接受到消息后回调此函数    
def on_message(client, userdata, msg): 
    print('\n'*5)   
    print("主题:"+msg.topic+" 消息:"+str(msg.payload)) 

    payload_length = len(msg.payload)
    print('-------payload_length---------')
    print(msg.payload)
    print(payload_length)
    un_int = struct.unpack(str(payload_length) + 'B', msg.payload)
    print(un_int)
    uints = list(un_int)
    print(uints)
    print(uints[0])
    print(type(uints[0]))

    if uints[0] == 49:
        print("gateway!")
        # query_device_distributed.delay(units)
        # query_device_distributed(units)
        foo()
    elif units[0] ==0:
        print("module")
        query_device.delay(units)


def foo():
    print('bar!')   



if __name__ == '__main__':

    client = mqtt.Client()    
    #参数有 Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")    
    client.on_connect = on_connect #设置连接上服务器回调函数    
    client.on_message = on_message  #设置接收到服务器消息回调函数    
    client.connect("localhost", 1883, 60)  #连接服务器,端口为1883,维持心跳为60秒    
    
    query_device_distributed.delay([1,1,1,0,0])

    client.loop_forever()