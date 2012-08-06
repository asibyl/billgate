from pytz import utc, timezone
from flask import render_template, g
from coaster.views import load_model
from billgate import app
from flask import render_template, redirect, url_for
from billgate.models.item import Item
from billgate.models.workspace import Workspace
from billgate.views.login import lastuser, requires_workspace_member

#tz = timezone(app.config['TIMEZONE'])


@app.context_processor
def sidebarvars():
    if hasattr(g, 'user'):
        # TODO: Need more advanced access control
        org_ids = g.user.organizations_memberof_ids()
    else:
        org_ids = []
    workspaces = Workspace.query.filter(Workspace.userid.in_(org_ids)).order_by('title').all()
    if hasattr(g, 'workspace'):
        return {
            'workspaces': workspaces,
            'items': Item.query.filter_by(workspace=g.workspace).order_by('title').all(),
            'permissions': lastuser.permissions(),
        }
    else:
        return {
            'workspaces': workspaces,
        }


@app.route('/')
def index():
    context = {
    }
    return render_template('index.html', **context)

@app.route('/<workspace>/')
@load_model(Workspace, {'name': 'workspace'}, 'workspace')
@requires_workspace_member
def workspace_view(workspace):
    return render_template('workspace.html', workspace=workspace)


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'), code=301)
