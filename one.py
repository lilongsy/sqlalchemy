#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    fullname = Column(String(20))
    passwd = Column(String(20))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.passwd)


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

engine = create_engine('mysql://root:123456@127.0.0.1:3306/alchemy', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
"""
// Insert Data
ed_user = User(name='ed', fullname='Ed Jone', passwd='password')
session.add(ed_user)

// Batch Insert Data
session.add_all([
    User(name='ll', fullname='ll China', passwd='china'),
    User(name='ll1', fullname='ll China', passwd='china'),
    User(name='ll2', fullname='ll China', passwd='china')
])

for user in session.query(User).order_by(User.id):
    print user.name
    print "Test "

// Select Data
jack = User(name='jack', fullname='Jack Bean', passwd='giffd')
jack.addresses = [Address(email_address="jack@126.com"), Address(email_address="j25@124.com")]
session.add(jack)

jack = session.query(User).filter_by(name='jack').one()
print jack.addresses
"""
print session.query(User).join(Address).filter(Address.email_address=='jack@126.com').all()
session.commit()
