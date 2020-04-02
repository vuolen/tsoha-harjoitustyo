from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.projects.models import Project
from application.projects.forms import CreateProjectForm, UpdateProjectForm
from application.permissions.models import Permission

@app.route("/projects", methods=["GET"])
@login_required
def projects_index():
    projects = db.engine.execute("SELECT * FROM project as P WHERE EXISTS (SELECT * FROM permission WHERE user_id=? AND project_id=P.id)", [current_user.get_id()])
    print(projects)
    return render_template("projects/list.html", projects = projects)

@app.route("/projects/new/")
@login_required
def projects_form():
    return render_template("projects/new.html", form = CreateProjectForm())

@app.route("/projects/", methods=["POST"])
@login_required
def projects_create():
    form = CreateProjectForm(request.form)

    if not form.validate():
        return render_template("projects/new.html", form = form)
    
    p = Project(form.name.data)
    db.session().add(p)
    db.session().commit()

    print(p.id)
    perm = Permission(p.id, current_user.get_id(), True)
    db.session().add(perm)
    db.session().commit()
    
    return redirect(url_for("projects_index"))

@app.route("/projects/<project_id>/")
@login_required
def projects_update_form(project_id):
    p = Project.query.get(project_id)
    return render_template("projects/update.html", project=p, form = UpdateProjectForm())

@app.route("/projects/<project_id>/", methods=["POST"])
@login_required
def projects_update_name(project_id):
    form = UpdateProjectForm(request.form)

    p = Project.query.get(project_id)
    
    if not form.validate():
        return render_template("/projects/update.html", project=p, form = form)

    p.name = form.name.data

    db.session().commit()

    return redirect(url_for("projects_update_form", project_id = project_id))
