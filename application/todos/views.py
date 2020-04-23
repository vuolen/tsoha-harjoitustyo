from flask import render_template, request, redirect, url_for
from flask_login import login_required

from application import app, db, permission_required
from application.todos.models import Todo
from application.projects.models import Project
from application.stages.models import Stage
from application.todos.forms import CreateTodoForm

@app.route("/projects/<project_id>/todos", methods=["GET"])
@permission_required()
@login_required
def todos_index(project_id):
    p = Project.query.get(project_id)
    return render_template("todos/index.html", project=p,
                           form = CreateTodoForm(),
                           most_populated_stage = Stage.get_most_populated_stage(project_id))


@app.route("/projects/<project_id>/todos", methods=["POST"])
@permission_required()
@login_required
def todos_create(project_id):
    form = CreateTodoForm(request.form)

    if not form.validate():
        return render_template("todos/index.html", form = form)

    t = Todo()
    t.stage_id = Stage.get_first_stage(project_id).id
    t.text = form.text.data
    db.session().add(t)
    db.session().commit()
    
    return redirect(url_for("todos_index", project_id = project_id))

@app.route("/projects/<project_id>/todos/<todo_id>/advance", methods=["GET"])
@permission_required()
@login_required
def todos_advance(project_id, todo_id):
    t = Todo.query.get(todo_id)
    next_stage_id = Stage.get_next_stage_id(project_id, t.stage_id)
    if next_stage_id is not None:
        t.stage_id = next_stage_id
        db.session().commit()
    
    return redirect(url_for("todos_index", project_id = project_id))

@app.route("/projects/<project_id>/todos/<todo_id>/delete", methods=["GET"])
@permission_required()
@login_required
def todos_delete(project_id, todo_id):
    t = Todo.query.get(todo_id)
    if t.stage.project_id == int(project_id):
        db.session().delete(t)
        db.session().commit()
    
    return redirect(url_for("todos_index", project_id = project_id))
