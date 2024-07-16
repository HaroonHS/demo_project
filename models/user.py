from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable= False)
    email = db.Column(db.String(80), nullable= False, unique=True)
    phone_number = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer,nullable= False)
    password = db.Column(db.String, nullable= False)

    reviews = db.relationship("ReviewModel", back_populates= "user", lazy="dynamic" )

    like = db.relationship("ReviewModel", back_populates= "likee", secondary ="likes")


    # followers = db.relationship('UserModel', 
    #                            secondary="supporters", 
    #                            primaryjoin=("supporters.user_id == id"), 
    #                            secondaryjoin=("supporters.supporter == id"), 
    #                            back_populates= "supporters", 
    #                            lazy='dynamic')


    # followed = db.relationship('User', 
    #                            secondary=supporters, 
    #                            primaryjoin=(supporters.c.follower_id == id), 
    #                            secondaryjoin=(followers.c.followed_id == id), 
    #                            backref=db.backref('followers', lazy='dynamic'), 
    #                            lazy='dynamic')

    # supporters = db.relationship("UserModel", back_populates= "followers", secondary="supporters")

    # followers = db.relationship("UserModel", back_populates= "supporters", secondary="supporters")

    #role = db.relationship("RoleModel", back_populates ="roles")
