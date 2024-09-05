from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    labels = db.Column(db.String(500), nullable=True)  # 用于存储标签


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label  = db.Column(db.String(500), nullable=True)  # 用于存储标签