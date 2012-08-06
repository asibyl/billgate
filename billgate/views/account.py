# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash, url_for
from coaster.views import load_model
from baseframe.forms import render_redirect, render_form
from billgate import app
from billgate.models import db, Profile, User, Item
from billgate.views.login import lastuser


@app.route('/account')
@lastuser.requires_login
def account_view():
	return render_template('account.html')