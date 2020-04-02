from flask import render_template
from flask_login import login_required

from application import app
from application.stages.models import Stage
from application.projects.models import Project


@app.route("/projects/<project_id>/stages")
@login_required
def stages_list(project_id):
    p = Project.query.get(project_id)
    stages = Stage.query.filter_by(project_id = project_id).order_by(Stage.index).all()
    return render_template("stages/list.html", project=p, stages=stages)
