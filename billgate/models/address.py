from billgate.models import User
from uuid import uuid4
from datetime import datetime

class Address(BaseScopedIdMixin, db.Model):
    __tablename__ = 'address'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relation(User, backref=db.backref('addresses', cascade='all, delete-orphan'))
    parent = db.synonym('user')

    name = db.Column(db.Unicode(1200), default=u'', nullable=True)
    address_text = db.Column(db.Unicode(1200), default=u'', nullable=True)
    city = db.Column(db.Unicode(1200), default=u'', nullable=True)
    state = db.Column(db.Unicode(1200), default=u'', nullable=True)
    postal_code = db.Column(db.Unicode(1200), default=u'', nullable=True)
    country = db.Column(db.Unicode(1200), default=u'', nullable=True)
       
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now) 
    updated_at = db.Column(db.DateTime, nullable=False)