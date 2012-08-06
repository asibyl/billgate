# -*- coding: utf-8 -*-

from flask import url_for
from flask.ext.lastuser.sqlalchemy import UserBase
from billgate.models import db

__all__ = ['User']


class User(UserBase, db.Model):
    __tablename__ = 'user'

    @property
    def profile_url(self):
    	return url_for('account')

    @property
    def profile(self):
    	return Profile.query.filter_by(userid=self.userid).first()

    @property
    def profiles(self):
    	return [self.profile] + Profile.query.filter(
    		Profile.userid.in_(self.organizations_owned_ids())).order_by('title').all()