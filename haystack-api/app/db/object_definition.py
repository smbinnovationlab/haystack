# -*- coding:utf-8 -*-

from sqlalchemy import Integer, Float, String, Text, Boolean, DateTime, Enum, BigInteger
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Site(Base):
    __tablename__ = 'site'
    site_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    domain = Column(String(255))
    full_url = Column(Text)
    is_finished = Column(Boolean, server_default='0')
    product_id = Column(String(36))
    debug_info = Column(Text)


class ProductEvent(Base):
    __tablename__ = 'product_event'
    event_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    site_id = Column(Integer, ForeignKey('site.site_id', ondelete='CASCADE'))
    event_time = Column(DateTime)
    event_type = Column(String(255), nullable=True)
    product_price = Column(Float(precision='11, 2'))
    product_currency = Column(String(255))
    product_status = Column(Enum('in stock', 'out of stock'), server_default='in stock')


class Product(Base):
    __tablename__ = 'product'
    product_id = Column(String(36), primary_key=True, nullable=False, unique=True)
    is_searching = Column(Boolean, server_default='1')
