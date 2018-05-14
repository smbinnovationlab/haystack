# -*- coding:utf-8 -*-

from sqlalchemy import Integer, Float, String, Text, Boolean, DateTime, Enum, BigInteger
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class URLData(Base):
    __tablename__ = 'url_data'
    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    url = Column(Text, nullable=False)
    price = Column(Float(precision='11, 2'))
    currency = Column(String(255))


class VendorProduct(Base):
    __tablename__ = 'vendor_product'
    product_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    product_name = Column(String(255))
    product_price = Column(Float(precision='11, 2'))
    currency = Column(String(255))
    is_favourite = Column(Boolean, server_default='0')
    last_avg_sale_price = Column(Float(precision='11, 2'))
    sku_id = Column(String(255))
    is_new = Column(Integer, server_default='1')


class Site(Base):
    __tablename__ = 'site'
    site_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    domain = Column(String(255))
    pattern_url = Column(String(255))
    full_url = Column(Text)
    country = Column(String(255), server_default='Unknown')
    site_type = Column(String(255), server_default='Unknown')
    last_indexed = Column(DateTime)
    status = Column(Boolean, server_default='0')


class ProductSite(Base):
    __tablename__ = 'product_site'
    product_site_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    product_id = Column(Integer, ForeignKey('vendor_product.product_id', ondelete='CASCADE'))
    site_id = Column(Integer, ForeignKey('site.site_id', ondelete='CASCADE'))


class ProductEvent(Base):
    __tablename__ = 'product_event'
    event_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    product_site_id = Column(Integer, ForeignKey('product_site.product_site_id', ondelete='CASCADE'))
    event_time = Column(DateTime)
    event_type = Column(String(255), nullable=True)
    product_name = Column(String(255))
    product_price = Column(Float(precision='11, 2'))
    currency = Column(String(255))
    product_status = Column(Enum('in stock', 'out of stock'), server_default='in stock')
    price_change = Column(Boolean, server_default='0')


class ProductImageUrl(Base):
    __tablename__ = 'product_image_url'
    image_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    image_url = Column(Text, nullable=False)
    product_id = Column(Integer, ForeignKey('vendor_product.product_id', ondelete='CASCADE'))


class ProductEventBak(Base):
    __tablename__ = 'product_event_bak'
    event_id = Column(Integer, primary_key=True, nullable=False)
    product_site_id = Column(Integer, ForeignKey('product_site.product_site_id', ondelete='CASCADE'))
    event_time = Column(DateTime)
    event_type = Column(String(255), nullable=True)
    product_name = Column(String(255))
    product_price = Column(Float(precision='11, 2'))
    currency = Column(String(255))
    product_status = Column(Enum('in stock', 'out of stock'), server_default='in stock')
    price_change = Column(Boolean, server_default='0')
