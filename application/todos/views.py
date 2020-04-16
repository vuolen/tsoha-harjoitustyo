from flask import render_template, request
from flask_login import login_required

from application import app, db
from application.projects.models import Project

@app.route("/projects/<project_id>/todos", methods=["GET"])
@login_required
def todos_index(project_id):
    p = Project.query.get(project_id)
    return render_template("todos/index.html", project=p)


@app.route("/projects/<project_id>/todos", methods=["POST"])
@login_required
def todos_create(project_id):
    
    return render_template("todos/index.html", project=p)
