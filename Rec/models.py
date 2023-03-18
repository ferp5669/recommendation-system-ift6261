from Rec import db, login_manager, app
from flask_login import UserMixin

# Getting the user from the user ID stored in a session
# Decoration added so the login_manager extension knows how to get a user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # How to display our user info
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
