from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db import ProductionLine, PLCProtocol, PLCType, DBType, Device
import json


connect = create_engine("mysql+pymysql://root:caojing1010@localhost:3306/damao",
                        encoding="utf-8",
                        echo=True)  # 连接数据库，echo=True =>把所有的信息都打印出来


Session = sessionmaker(bind=connect)
session = Session()



session.add_all([
    ProductionLine(id=1, name='line1'),
    ProductionLine(id=2, name='line2'),
    ProductionLine(id=3, name='line3'),
    ProductionLine(id=4, name='line4'),
    ProductionLine(id=5, name='line5'),
    ProductionLine(id=6, name='line6'),
    ProductionLine(id=7, name='line7'),
    ProductionLine(id=8, name='line8'),
    ProductionLine(id=9, name='line9'),
    ProductionLine(id=10, name='line10')
])





session.add_all([
    PLCProtocol(id=1, name='Mitsubishi_1'),
    PLCProtocol(id=2, name='Mitsubishi_2'),
    PLCProtocol(id=3, name='Mitsubishi_3'),
    PLCProtocol(id=4, name='Mitsubishi_4'),
    PLCProtocol(id=5, name='Mitsubishi_5'),
    PLCProtocol(id=6, name='siemens_1'),
    PLCProtocol(id=7, name='siemens_2'),
    PLCProtocol(id=8, name='siemens_3'),
    PLCProtocol(id=9, name='omron_1'),
    PLCProtocol(id=10, name='omron_2')
])




session.add_all([
    PLCType(id=1, name='Mitsubishi_fx1s', PLCProtocol_id=1),
    PLCType(id=2, name='Mitsubishi_fx1n', PLCProtocol_id=1),
    PLCType(id=3, name='Mitsubishi_fx2n', PLCProtocol_id=1),
    PLCType(id=4, name='Mitsubishi_fx3u', PLCProtocol_id=1),
    PLCType(id=5, name='Mitsubishi_fx3g', PLCProtocol_id=1),
    PLCType(id=6, name='Mitsubishi_fx3ga', PLCProtocol_id=1),
    PLCType(id=7, name='Mitsubishi_fxq', PLCProtocol_id=2),
    PLCType(id=8, name='siemens_smart20', PLCProtocol_id=6),
    PLCType(id=9, name='siemens_1200', PLCProtocol_id=6),
    PLCType(id=10, name='siemens_1500', PLCProtocol_id=6),
])





session.add_all([
    DBType(id=1, name='sqlserver'),
    DBType(id=2, name='mysql'),
    DBType(id=3, name='postgresql'),
    DBType(id=4, name='oracle'),
    DBType(id=5, name='sqlite'),
    DBType(id=6, name='access'),
])






plc_parameter_dict = {"plc_parameter":[
{"parameter":"p1",
"address":"m200",
"datatype":"double"},

{"parameter":"p2",
"address":"m100",
"datatype":"double"},
]}


DB_fields_dict = {"DB_fields":[
{"parameter":"p1",
"field":"p1",
"datatype":"double"},

{"parameter":"p2",
"field":"p2",
"datatype":"double"},
]}


session.add_all([
    Device(id=1, name='device1', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.101",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=2, name='device2', productline_id=1, isPLC=False, DBType_id=2, DB_host="192.168.0.200", DB_port="3306", DB_name="mysql_test", DB_user="user", DB_password="password", DB_field=json.dumps(DB_fields_dict),),
    Device(id=3, name='device3', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.103",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=4, name='device4', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.104",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=5, name='device5', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.105",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=6, name='device6', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.106",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=7, name='device7', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.107",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=8, name='device8', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.108",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=9, name='device9', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.109",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=10, name='device10', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.110",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=11, name='device11', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.111",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=12, name='device12', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.112",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=13, name='device13', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.113",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=14, name='device14', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.114",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=15, name='device15', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.115",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=16, name='device16', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.116",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=17, name='device17', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.117",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=18, name='device18', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.118",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=19, name='device19', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.119",plc_parameter=json.dumps(plc_parameter_dict),),
    Device(id=20, name='device20', productline_id=1, isPLC=True, PLCType_id=4, plc_ip="192.168.0.120",plc_parameter=json.dumps(plc_parameter_dict),),

])


session.commit()




lines = session.query(ProductionLine).all()
#打印实例
print(lines)
for line in lines:
#打印结果
	print(line.id,line.name,)



devices = session.query(Device).all()
#打印实例
print(devices)
for device in devices:
#打印结果
	print(device.id,device.name,)



# class ProductionLine(Base):
#     __tablename__ = "production_line"  # 表名
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200))
#     devices = relationship("Device", backref="production_line")


# class PLCProtocol(Base):
#     __tablename__ = "PLCProtocol"  # 表名
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200))
#     devices = relationship("PLCType", backref="PLCProtocol")


# class PLCType(Base):
#     __tablename__ = "PLCType"  # 表名
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200))
#     PLCProtocol_id = Column(Integer, ForeignKey('PLCProtocol.id'))
#     devices = relationship("Device", backref="PLCType")


# class DBType(Base):
#     __tablename__ = "DBType"  # 表名
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200))
#     devices = relationship("Device", backref="DBType")


# class Device(Base):
#     __tablename__ = "device"  # 表名
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200))
#     productline_id = Column(Integer, ForeignKey('production_line.id'))
#     isPLC = Column(Boolean)
#     PLCType_id = Column(Integer, ForeignKey('PLCType.id'))
#     plc_ip = Column(String(100))
#     plc_parameter = Column(String(1000)) #json string,parameter and data type
#     DBType_id = Column(Integer, ForeignKey('DBType.id'))
#     DB_host = Column(String(30)) 
#     DB_port = Column(String(10)) 
#     DB_name = Column(String(50)) 
#     DB_user = Column(String(100)) 
#     DB_password = Column(String(100)) 
#     DB_field = Column(String(1000)) #json string,field and data type

