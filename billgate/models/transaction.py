from decimal import Decimal
from datetime import datetime
from billgate.models import db, BaseScopedIdMixin
from billgate.models.user import User
from billgate.models.workspace import Workspace
from datetime import datetime

__all__ = ['Transaction', 'TRANSACTION_STATUS']

class TRANSACTION_STATUS:
    INITIATED = 0
    APPROVED = 1
    ADDRESSED = 2
    CONFIRMED = 3
    PAYMENT_INITIATED = 4
    PAYMENT_REQ_RETURNED = 5
    REFUNDED = 6

# draft invoice, to add function to create invoice on api request or transaction completion
class Transaction(BaseScopedIdMixin, db.Model):
    __tablename__ = 'transaction'

    #: Organization workspace where this transaction is accepted 
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relation(Workspace, backref=db.backref('transactions', cascade='all, delete-orphan'))
    parent = db.synonym('workspace')

    #: User who submitted the transaction
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, primaryjoin=user_id == User.id, 
        backref=db.backref('transactions', cascade='all, delete-orphan'))

    #: Date of transaction submission
    datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    #: Currency for items in this transaction
    currency = db.Column(db.Unicode(3), nullable=False, default=u'INR')

    #: Total value in the transaction's currency
    total_value = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal('0.0'))

    b_name = db.Column(db.Unicode(250), default=u'', nullable=True)
    b_address = db.Column(db.Unicode(1200), default=u'', nullable=True)
    b_city = db.Column(db.Unicode(250), default=u'', nullable=True)
    b_state = db.Column(db.Unicode(250), default=u'', nullable=True)
    b_country = db.Column(db.Unicode(250), default=u'', nullable=True)
    b_postalcode = db.Column(db.Unicode(6), default=u'', nullable=True)

    #updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    status = db.Column(db.Integer, nullable=False, default=TRANSACTION_STATUS.INITIATED)
    
    __table_args__ = (db.UniqueConstraint('url_id', 'workspace_id'),)
