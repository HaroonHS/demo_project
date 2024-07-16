from db import db

class ReviewModel(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key = True)
    brandname = db.Column(db.String(80), nullable= False)
    product = db.Column(db.String(100), nullable= False)
    review = db.Column(db.String(256), nullable= False)
    files = db.Column(db.String(256), nullable= False)
    rating  = db.Column(db.Integer, nullable= False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)

    user = db.relationship("UserModel", back_populates= "reviews")

    likee = db.relationship("UserModel", back_populates= "like", secondary ="likes")