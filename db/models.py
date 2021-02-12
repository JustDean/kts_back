from db.db_accessor import db


class User(db.Model):
    __tablename__ = "users"

    u_id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

