from flask import redirect, url_for, render_template, request
from flask_login import login_required

from application import app, db, permission_required
from application.permissions.forms import AddUserToProjectForm
from application.permissions.models import Permission
from application.projects.models import Project
from application.projects.forms import UpdateProjectForm
from application.stages.forms import CreateStageForm


@app.route("/projects/<project_id>/permissions", methods=["POST"])
@login_required
@permission_required(admin = True)
def permissions_create(project_id):
    form = AddUserToProjectForm(project_id, request.form)

    p = Project.query.get(project_id)
    
    if not form.validate():
        return render_template("projects/update.html", project = p,
                               add_user_to_project_form = form,
                               project_form = UpdateProjectForm(),
                               stage_form = CreateStageForm())

    print(form.username.data)
    print(form.admin.data)
    perm = Permission(project_id, form.username.data, form.admin.data)
    db.session().add(perm)
    db.session().commit()
    
    return redirect(url_for("projects_update_form", project_id = project_id))

@app.route("/projects/<project_id>/permissions/<permission_id>/delete", methods=["GET"])
@login_required
@permission_required(admin = True)
def permissions_delete(project_id, permission_id):
    p = Permission.query.get(permission_id)
    
    if p is not None and p.project_id == int(project_id):
        db.session().delete(p)
        db.session().commit()
    
    return redirect(url_for("projects_update_form", project_id = project_id))
