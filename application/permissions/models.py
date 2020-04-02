from application import db
from application.models import Base

class Permission(Base):
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
