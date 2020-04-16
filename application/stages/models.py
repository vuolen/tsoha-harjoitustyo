from sqlalchemy import text

from application import db
from application.models import Base

class Stage(Base):
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    index = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    todos = db.relationship("Todo", backref="stage", lazy=True)

    @classmethod
    def get_first_stage(self, project_id):
        first_stage = Stage.query.filter_by(project_id = project_id).order_by(Stage.index).first()
        return first_stage
    
    @classmethod
    def get_new_index(self, project_id):
        last_stage = Stage.query.filter_by(project_id = project_id).order_by(Stage.index.desc()).first()
        if last_stage is None:
            return 0

        return last_stage.index + 1

    @classmethod
    def get_next_stage_id(self, project_id, stage_id):
        s = Stage.query.get(stage_id)
        next_stage = Stage.query.filter_by(project_id = project_id).filter(Stage.index > s.index).first()
        return next_stage.id

    @classmethod
    def get_most_populated_stage(self, project_id):
        stmt = text("SELECT Stage.name,COUNT(*) FROM Stage"
                    " JOIN Todo"
                    " ON Stage.id = Todo.stage_id"
                    " GROUP BY Stage.id"
                    " ORDER BY COUNT(*) DESC")

        res = db.engine.execute(stmt)
        most_populated_stage = res.first()
        if most_populated_stage is None:
            return None

        return most_populated_stage[0]
