from flask.ext.wtf import Form, TextField, IntegerField, DecimalField, SelectField
from billgate.models.item import ITEM_STATUS_CODES

from billgate import app


class ItemForm(Form):
    name = TextField('Name', validators=[Required()])
    nos_available = IntegerField("No. Available", description="The number of items available in the inventory", default=50, validators=[Required()])
    price_before_tax = TextField('Price Before Tax', validators=[Required()])
    tax_rate = DecimalField("Tax Rate", places=2, validators=[Required(), NumberRange(0, 100)])
    status = SelectField('Status', validators=[Required()], default='D',
        choices=ITEM_STATUS_CODES)