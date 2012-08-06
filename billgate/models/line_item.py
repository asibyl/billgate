from decimal import Decimal
from datetime import datetime
from flask import url_for
from billgate.models import db, BaseMixin, BaseScopedNameMixin
from billgate.models.user import User
from billgate.models.workspace import Workspace


__all__ = ['Item','ITEM_STATUS', 'LineItem']


# Item that can be purchased, along with inventory available and price
class LineItem(BaseMixin, db.Model):
    __tablename__ = 'Item'
    
    #: Type of LineItem
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship(Category, primaryjoin=item_id == Item.id)

    #: Transaction to which this line item belongs
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    transaction = db.relationship(Transaction, primaryjoin=transaction_id == Transaction.id, 
        backref=db.backref('line_items', cascade='all, delete-orphan'))
    parent = db.synonym('transaction')

    quantity = db.Column(db.Integer, default=1, nullable=False)
    line_amount_before_tax = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal('0.0'))
    line_total = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal('0.0'))

    def update_line_total(self):
        #calculate line total
        self.line_total = self.quantity * self.item.price_before_tax * self.item.tax_rate
