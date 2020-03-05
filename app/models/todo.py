from app.db import db


class TodoModel(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Unicode())
    completed = db.Column(db.Boolean(), default=False)

    user_id = db.Column(None, db.ForeignKey('user.id'))
