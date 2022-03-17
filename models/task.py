from utils.db import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    # status: new, in progress, done
    status = db.Column(db.String(15), nullable=False)

    def __init__(self, userId, description, status="new") -> None:
        self.userId = userId
        self.description = description
        self.status = status

    def __repr__(self) -> str:
        return f"Task({self.id}, {self.userId}, '{self.description}', '{self.status}')"
