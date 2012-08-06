from flask.ext.wtf import Form, RadioField, SelectField

CURRENCIES = [
    ('INR', 'INR - India Rupee'),
    ('USD', 'USD - US Dollar'),
    ('EUR', 'EUR - Euro'),
    ('GBP', 'GBP - Great Britain Pound'),
    ('SGD', 'SGD - Singapore Dollar'),
    ]


class NewWorkspaceForm(Form):
    """
    Create a workspace.
    """
    workspace = RadioField(u"Organization", validators=[Required()],
        description=u"Select the organization you’d like to create a workspace for.")
    currency = SelectField(u"Currency", validators=[Required()], choices=CURRENCIES,
        description=u"The standard currency for your organization’s accounts.")