# -*- coding: utf-8 -*-

"""
Setup Workspace, Create and Manage Items
"""

from flask import flash, url_for, render_template, g
from coaster.views import load_model, load_models
from baseframe.forms import render_form, render_redirect, render_delete_sqla, render_message

from billgate import app
from billgate.views.login import lastuser, requires_workspace_member, requires_workspace_owner
from billgate.models import db, Item, Workspace
from billgate.forms import ItemForm, NewWorkspaceForm


@app.route('/new', methods=['GET', 'POST'])
@lastuser.requires_login
def workspace_new():
    # Step 1: Get a list of organizations this user owns
    existing = Workspace.query.filter(Workspace.userid.in_(g.user.organizations_owned_ids())).all()
    existing_ids = [e.userid for e in existing]
    # Step 2: Prune list to organizations without a workspace
    new_workspaces = []
    for org in g.user.organizations_owned():
        if org['userid'] not in existing_ids:
            new_workspaces.append((org['userid'], org['title']))
    if not new_workspaces:
        return render_message(
            title=u"No organizations remaining",
            message=u"You do not have any organizations that do not yet have a workspace.")

    # Step 3: Ask user to select organization
    form = NewWorkspaceForm()
    form.workspace.choices = new_workspaces
    if form.validate_on_submit():
        # Step 4: Make a workspace
        org = [org for org in g.user.organizations_owned() if org['userid'] == form.workspace.data][0]
        workspace = Workspace(name=org['name'], title=org['title'], userid=org['userid'],
            currency=form.currency.data)
        db.session.add(workspace)
        db.session.commit()
        flash("Created new workspace for %s" % workspace.title, "success")
        return render_redirect(url_for('workspace_view', workspace=workspace.name), code=303)
    return render_form(form=form, title="Create a new organization workspace", submit="Create",
        formid="workspace_new", cancel_url=url_for('index'), ajax=False)


@app.route('/<workspace>/items/')
@load_model(Workspace, {'name': 'workspace'}, 'workspace')
@requires_workspace_member
def item_list(workspace):
    return render_template('items.html')


@app.route('/<workspace>/items/new', methods=['GET', 'POST'])
@load_model(Workspace, {'name': 'workspace'}, 'workspace')
@requires_workspace_owner
def item_new(workspace):
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(workspace=workspace)
        form.populate_obj(budget)
        item.make_name()
        db.session.add(item)
        db.session.commit()
        flash("Created new item '%s'." % item.name, "success")
        return render_redirect(url_for('item', workspace=workspace.name, item=item.name), code=303)
    return render_form(form=form, title=u"Create new item",
        formid="item_new", submit=u"Create",
        cancel_url=url_for('item_list', workspace=workspace.name), ajax=True)


@app.route('/<workspace>/items/<item>/edit', methods=['GET', 'POST'])
@load_models(
    (Workspace, {'name': 'workspace'}, 'workspace'),
    (Item, {'name': 'item', 'workspace': 'workspace'}, 'item')
    )
@requires_workspace_owner
def item_edit(workspace, item):
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        item.make_name()
        db.session.commit()
        flash("Edited item '%s'" % item.name, "success")
        return render_redirect(url_for('item', workspace=workspace.name, item=item.name), code=303)
    return render_form(form=form, title=u"Edit Item",
        formid='item_edit', submit=u"Save",
        cancel_url=url_for('item', workspace=workspace.name, item=item.name), ajax=True)


#@app.route('/<workspace>/budgets/<budget>/delete', methods=['GET', 'POST'])
#@load_models(
#    (Workspace, {'name': 'workspace'}, 'workspace'),
#    (Budget, {'name': 'budget', 'workspace': 'workspace'}, 'budget')
#    )
#@requires_workspace_owner
#def budget_delete(workspace, budget):
#    return render_delete_sqla(budget, db, title=u"Confirm delete",
#        message=u"Delete budget '%s'?" % budget.title,
#        success=u"You have deleted budget '%s'." % budget.title,
#        next=url_for('budget_list', workspace=workspace.name))
