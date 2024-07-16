from db import db

class PermissionModel(db.Model):
    __tablename__ = "role_permissions"

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    permissions = db.Column(db.BLOB(), nullable=False)
    
    #users = db.relationship("UserModel", back_populates ="role",lazy = "dynamic")