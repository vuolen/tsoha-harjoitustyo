from application import db
from application.models import Base

class Project(Base):
    name = db.Column(db.String(144), nullable=False)

    stages = db.relationship("Stage", backref="project", lazy=True)
    
    def __init__(self, name):
        self.name = name;
