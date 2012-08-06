# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from billgate import app
from coaster.sqlalchemy import BaseMixin, BaseNameMixin, BaseScopedNameMixin, BaseScopedIdNameMixin, BaseScopedIdMixin

db = SQLAlchemy(app)

from billgate.models.user import *
