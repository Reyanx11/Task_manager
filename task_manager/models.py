from task_manager import db,bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    email = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(16), nullable = False)


def __repr__(self):
    return f"User('{self.username}', '{self.email}')"



