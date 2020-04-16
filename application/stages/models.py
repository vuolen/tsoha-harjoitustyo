from application import db
from application.models import Base

class Stage(Base):
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    index = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    todos = db.relationship("Todo", backref="stage", lazy=True)

    
    @classmethod
    def get_next_index(self, project_id):
        last_stage = Stage.query.filter_by(project_id = project_id).order_by(Stage.index.desc()).first()
        if last_stage is None:
            return 0

        return last_stage.index + 1
