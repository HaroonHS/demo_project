import os
import uuid
from flask import request,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,get_jti,get_jwt_identity

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from db import db
from blocklist import BLOCKLIST
from models import ReviewModel,UserModel

from schemas import ReviewSchema,ReviewLikeSchema,TestReview

blp = Blueprint("reviews",__name__,description="operation on reviews")

@blp.route("/reviews")
class Reviews(MethodView):
    @blp.response(200,ReviewSchema(many=True))
    def get(self):
        review = ReviewModel.query.all()

        return review
    

    
    @blp.arguments(ReviewSchema)
    @blp.response(200,ReviewSchema)
    def post(self,review_data):
        review = ReviewModel(**review_data)
        # review  = ReviewModel(
        #                    product = review_data['product'],
                    
        #  )

        try :
            db.session.add(review)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message =str(e))
        return review
    



@blp.route("/review/<int:user_id>")
class UserRviews(MethodView):
    @blp.response(200,ReviewSchema(many=True))
    def get(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        return user.reviews.all()
    


    @blp.arguments(ReviewSchema)
    @blp.response(200,ReviewSchema)
    def post(self,review_data,user_id):
        review = ReviewModel(**review_data,user_id=user_id)
        # review  = ReviewModel(
        #                    product = review_data['product'],
                    
        #  )

        try :
            db.session.add(review)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message =str(e))
        return review

@blp.route("/like")
class ReviewLikes(MethodView):
    @blp.arguments(ReviewLikeSchema)
    @blp.response(200,ReviewSchema)
    def post(self,review_data):
        user = UserModel.query.get_or_404(review_data['user_id'])
        Review = ReviewModel.query.get_or_404(review_data['review_id'])

        user.like.append(Review)    

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occur ")
    
        return Review
    

@blp.route("/reviewss/<int:review_id>")
class UserRviews(MethodView):
    @blp.response(200,ReviewSchema(many=True))
    def get(self,review_id):
        review = ReviewModel.query.filter(ReviewModel.id == review_id)
        #return {"reiw":"ji"}
        return review



