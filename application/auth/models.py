from application import db
from application.models import Base

from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    fullname = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    permissions = db.relationship("Permission", backref="user")
    
    def __init__(self, username, fullname, password):
        self.username = username
        self.fullname = fullname
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_projects(self):
        stmt = text("SELECT * FROM project as P WHERE EXISTS (SELECT * FROM permission WHERE user_id=:userid AND project_id=P.id)").params(userid=self.get_id())
        res = db.engine.execute(stmt)
        
        return res

    def has_permission_to_project(self, project_id, admin):
        for permission in self.permissions:
            if admin and not permission.admin:
                continue
            if permission.project_id == project_id:
                return True
        return False
