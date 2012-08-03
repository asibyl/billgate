# -*- coding: utf-8 -*-

from flask.ext.lastuser.sqlalchemy import UserBase
from billgate.models import db

__all__ = ['User']


class User(UserBase, db.Model):
    __tablename__ = 'user'

    name = db.Column(db.Unicode(1200), default=u'', nullable=True)
    email = db.Column(db.Unicode(80), default=u'', nullable=True)
    phone_no = db.Column(db.Unicode(15), default=u'', nullable=True)
