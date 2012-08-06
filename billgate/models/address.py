from billgate.models import db, BaseScopedIdMixin
from billgate.models import User
from uuid import uuid4
from datetime import datetime

__all__ = ['Address']

class Address(BaseScopedIdMixin, db.Model):
    __tablename__ = 'address'
    
    # address must be unique within a user scope
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relation(User, backref=db.backref('addresses', cascade='all, delete-orphan'))
    parent = db.synonym('user')

    # selected address can be different from user name, etc.
    # will be assigned to transaction b_address, etc.
    name = db.Column(db.Unicode(250), default=u'', nullable=True)
    address = db.Column(db.Unicode(1200), default=u'', nullable=True)
    city = db.Column(db.Unicode(250), default=u'', nullable=True)
    state = db.Column(db.Unicode(250), default=u'', nullable=True)
    postal_code = db.Column(db.Unicode(6), default=u'', nullable=True)
    country = db.Column(db.Unicode(250), default=u'', nullable=True) 