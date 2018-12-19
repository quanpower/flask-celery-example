
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
 
connect = create_engine("mysql+pymysql://root:caojing1010@localhost:3306/damao",
                        encoding="utf-8",
                        echo=True)  # 连接数据库，echo=True =>把所有的信息都打印出来
 
 
Base = declarative_base()  # 生成ORM基类
 
 
class ProductionLine(Base):
    __tablename__ = "ProductionLine"  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    devices = relationship("Device", backref="production_line")


class PLCProtocol(Base):
    __tablename__ = "PLCProtocol"  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    PLCTypes = relationship("PLCType", backref="PLC_protocol")


class PLCType(Base):
    __tablename__ = "PLCType"  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    PLCProtocol_id = Column(Integer, ForeignKey('PLCProtocol.id'))
    devices = relationship("Device", backref="PLC_type")


class DBType(Base):
    __tablename__ = "DBType"  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    devices = relationship("Device", backref="DB_Type")


class Device(Base):
    __tablename__ = "Device"  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    productline_id = Column(Integer, ForeignKey('ProductionLine.id'))
    isPLC = Column(Boolean)
    PLCType_id = Column(Integer, ForeignKey('PLCType.id'))
    plc_ip = Column(String(100))
    plc_parameter = Column(String(1000)) #json string,parameter and data type
    DBType_id = Column(Integer, ForeignKey('DBType.id'))
    DB_host = Column(String(30)) 
    DB_port = Column(String(10)) 
    DB_name = Column(String(50)) 
    DB_user = Column(String(100)) 
    DB_password = Column(String(100)) 
    DB_field = Column(String(1000)) #json string,field and data type


Base.metadata.create_all(connect)   # 创建表结构

