from db.db_accessor import db


class Message(db.Model):
    __tablename__ = "user"

    u_id = db.Column(db.Integer, primary_key=True)
