from application import db
from application.models import Base

class Project(Base):
    name = db.Column(db.String(144), nullable=False)

    stages = db.relationship("Stage", backref="project", lazy=True)
    users = db.relationship("Permission", backref="project")
    
    def __init__(self, name):
        self.name = name;
