from application import db

class Permission(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"),
                           nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("account.id"),
                        nullable=False, primary_key=True)
    admin = db.Column(db.Boolean, primary_key=True, nullable=False)

    def __init__(self, project_id, user_id, admin):
        self.project_id = project_id
        self.user_id = user_id
        self.admin = admin
