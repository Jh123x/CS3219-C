import time
from . import db

class TodoItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(1000))
    date = db.Column(db.BigInteger, nullable=False, default=int(time.time()))
    is_complete = db.Column(db.Boolean(), nullable=False, default=False)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<Todo {self.id}>"
