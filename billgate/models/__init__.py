# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from billgate import app
from coaster.sqlalchemy import IdMixin, TimestampMixin, BaseMixin, BaseNameMixin

db = SQLAlchemy(app)

from billgate.models.user import *
