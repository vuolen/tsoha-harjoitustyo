from flask import render_template, request, redirect, url_for
from flask_login import login_required

from application import app, db
from application.projects.models import Project
from application.projects.forms import ProjectForm

@app.route("/projects", methods=["GET"])
def projects_index():
    return render_template("projects/list.html", projects = Project.query.all())

@app.route("/projects/new/")
@login_required
def projects_form():
    return render_template("projects/new.html", form = ProjectForm())

@app.route("/projects/", methods=["POST"])
@login_required
def projects_create():
    form = ProjectForm(request.form)

    if not form.validate():
        return render_template("projects/new.html", form = form)
    
    p = Project(form.name.data)
    db.session().add(p)
    db.session().commit()
    return redirect(url_for("projects_index"))

@app.route("/projects/<project_id>/")
@login_required
def projects_update_form(project_id):
    p = Project.query.get(project_id)
    return render_template("projects/update.html", project=p)

@app.route("/projects/<project_id>/", methods=["POST"])
@login_required
def projects_update_name(project_id):
    p = Project.query.get(project_id)
    p.name = request.form.get("name")

    db.session().commit()

    return redirect(url_for("projects_update_form", project_id = project_id))
