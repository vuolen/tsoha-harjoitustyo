from flask import redirect, url_for, render_template, request
from flask_login import login_required

from application import app, db, permission_required
from application.projects.models import Project
from application.stages.models import Stage
from application.projects.forms import UpdateProjectForm
from application.stages.forms import CreateStageForm


@app.route("/projects/<project_id>/stages", methods=["POST"])
@login_required
@permission_required(admin = True)
def stages_create(project_id):
    form = CreateStageForm(request.form)

    p = Project.query.get(project_id)

    if not form.validate():
        return render_template("projects/update.html", project = p,
                               stage_form = form,
                               project_form = UpdateProjectForm())
    
    s = Stage()
    s.project_id = project_id
    s.index = Stage.get_new_index(project_id)
    s.name = form.name.data
    db.session().add(s)
    db.session().commit()
    
    return redirect(url_for("projects_update_form", project_id = project_id))

@app.route("/projects/<project_id>/stages/<index>", methods=["GET"])
@login_required
@permission_required(admin = True)
def stages_delete(project_id, index):
    stage = Stage.query.filter_by(project_id = project_id, index = index).first()

    if stage is not None:
        db.session().delete(stage)
        db.session().commit()
    
    return redirect(url_for("projects_update_form", project_id = project_id))
