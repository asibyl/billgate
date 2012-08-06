from decimal import Decimal
from billgate.models import db, BaseScopedNameMixin
from billgate.models.workspace import Workspace

class ITEM_STATUS:
	DRAFT = 0
	LIVE = 1
	EXPIRED = 2

ITEM_STATUS_CODES = [
    ["D", "Draft"],
    ["L", "Live"],
    ["E", "Expired"]
]


# Item that can be purchased, along with inventory available and price
class Item(BaseScopedNameMixin, db.Model):
    __tablename__ = 'Item'

    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relation(Workspace, backref=db.backref('items', cascade='all, delete-orphan'))
    parent = db.synonym('workspace')
    __table_args__ = (db.UniqueConstraint('name', 'workspace_id'),)
    
    nos_available = db.Column(db.Integer, default=0, nullable=True)
    price_before_tax = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal('0.0'))
    tax_rate = db.Column(db.Numeric(0, 4), nullable=False, default=Decimal('0.0'))
    status = db.Column(db.Integer, default=ITEM_STATUS.DRAFT, nullable=False)