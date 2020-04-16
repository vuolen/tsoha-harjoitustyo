from flask import redirect, url_for, render_template, request
from flask_login import login_required

from application import app, db
from application.projects.models import Project
from application.stages.models import Stage
from application.stages.forms import CreateStageForm


@app.route("/projects/<project_id>/stages", methods=["GET"])
@login_required
def stages_index(project_id):
    p = Project.query.get(project_id)
    return render_template("stages/index.html", project=p, form = CreateStageForm())

@app.route("/projects/<project_id>/stages", methods=["POST"])
@login_required
def stages_create(project_id):
    form = CreateStageForm(request.form)

    if not form.validate():
        return render_template("stages/index.html", form = form)
    
    s = Stage()
    s.project_id = project_id
    s.index = Stage.get_new_index(project_id)
    s.name = form.name.data
    db.session().add(s)
    db.session().commit()
    
    return redirect(url_for("stages_index", project_id = project_id))

@app.route("/projects/<project_id>/stages/<index>", methods=["GET"])
@login_required
def stages_delete(project_id, index):
    stage = Stage.query.filter_by(project_id = project_id, index = index).first()

    if stage is not None:
        db.session().delete(stage)
        db.session().commit()
    
    return redirect(url_for("stages_index", project_id = project_id))
