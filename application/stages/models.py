from application import db
from application.models import Base

class Stage(Base):
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    index = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
