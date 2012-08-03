from billgate.models import User
from uuid import uuid4
from datetime import datetime

class PAYMENT_STATUS:
    INFO_REQD = 0
    SUBMITTED = 1
    FAILED = 2
    COMPLETED = 3
    CANCELLED = 4
    REJECTED = 5
    REFUNDED = 6

class Payment(BaseScopedIdMixin, db.Model):
    __tablename__ = 'payment'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relation(User, backref=db.backref('payments', cascade='all, delete-orphan'))
    parent = db.synonym('user')

    status = db.Column(db.Integer, nullable=False, default=PAYMENT_STATUS.INFO_REQD)
    amount = db.Column(db.Float, default=0.0, nullable=True)
    response = db.Column(db.Unicode(1200), default=u'', nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now) 
    updated_at = db.Column(db.DateTime, nullable=False)


    def _get_responseAsDict(self):
        if self.response:
            return eval(self.response)
        else:
            return {} # be careful with None and empty dict

    def _set_responseAsDict(self, value):
        if value:
            self.response = str(value)
        else:
            self.response = None

    response = property(_get_responseAsDict, _set_responseAsDict)
