from db import db

class RoleModel(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False,unique=True)
    status = db.Column(db.Integer)
    
    #user = db.relationship("UserModel", back_populates ="user",lazy = "dynamic")