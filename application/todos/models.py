from application import db
from application.models import Base

class Todo(Base):
    stage_id = db.Column(db.Integer, db.ForeignKey("stage.id"))
    todo = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name;

