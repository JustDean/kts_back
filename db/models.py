from db.db_accessor import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)


class Quiz(db.Model):
    __tablename__ = "quiz"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer_1 = db.Column(db.String)
    answer_2 = db.Column(db.String)
    answer_3 = db.Column(db.String)
    correct_answer = db.Column(db.String)
