from application import db
from application.models import Base

class Todo(Base):
    stage_id = db.Column(db.Integer, db.ForeignKey("stage.id"))
    text = db.Column(db.String, nullable=False)

