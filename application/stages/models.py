from sqlalchemy import text, UniqueConstraint

from application import db
from application.models import Base

class Stage(Base):
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)

    todos = db.relationship("Todo", backref="stage", lazy=True)

    __table_args__ = (UniqueConstraint("project_id", "index", name="project_index_uc"),)

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
        next_stage = Stage.query.filter_by(project_id = project_id).filter(Stage.index > s.index).order_by(Stage.index).first()
        if next_stage is None:
            return None
        return next_stage.id

    @classmethod
    def get_previous_stage_id(self, project_id, stage_id):
        s = Stage.query.get(stage_id)
        previous_stage = Stage.query.filter_by(project_id = project_id).filter(Stage.index < s.index).order_by(Stage.index.desc()).first()
        if previous_stage is None:
            return None
        return previous_stage.id

    @classmethod
    def swap_stage_indices(self, project_id, stage1_id, stage2_id):
        stage1 = Stage.query.get(stage1_id)
        stage2 = Stage.query.get(stage2_id)
        if stage1 is None or stage2 is None or stage1.project_id != project_id or stage2.project_id != project_id:
            return None
        # You cannot simply swap two unique values
        tmp1 = stage1.index
        tmp2 = stage2.index
        
        stage1.index = -1
        stage2.index = -2
        db.session.commit()

        stage1.index = tmp2
        stage2.index = tmp1
        db.session.commit()
        
        return True

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
