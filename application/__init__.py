from flask import Flask, render_template
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kanban.db"
    #app.config["SQLALCHEMY_ECHO"] = True
    
db = SQLAlchemy(app)

# kirjautuminen
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

from functools import wraps

def permission_required(admin = False):
    def callable(func):
        @wraps(func)
        def wrapper(*args, **kwargs):      
            if not current_user.has_permission_to_project(int(kwargs['project_id']), admin):
                return render_template("access_denied.html")
            return func(*args, **kwargs)
        return wrapper
    return callable


from application import views

from application.projects import models, views

from application.permissions import models

from application.auth import models, views

from application.stages import models, views

from application.todos import models, views

from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.create_all()
