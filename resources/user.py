import os
import uuid
from flask import request,url_for,redirect,session,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jti,get_jwt_identity

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from db import db
from blocklist import BLOCKLIST
from models import UserModel,ReviewModel,SupporterModel

from schemas import Userschema, UserUpdateSchema, UserLoginSchema, FilterSchema, FileformSchema,ReviewSchema,SupporterSchema
from flask_mail import Message,Mail
from authlib.integrations.flask_client import OAuth
from marshmallow import Schema, fields, validate


mail= Mail()

blp = Blueprint("users",__name__,description="operation on users")

@blp.route("/user/<int:page>")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200,Userschema(many=True))
    def get(self,page):
        per_page= 5
        #users = UserModel.query.all()
        users = UserModel.query.paginate(page=page,per_page=per_page)
        user_data = Userschema(many=True)
        data = user_data.dump(users)
        #users.revreviews()
        return jsonify({"status" : 200, "message" : "success", "body" : data, "error" :""  })
        return users
    
@blp.route("/user")
class UserAdd(MethodView):    
    @blp.arguments(Userschema)
    @blp.response(200,Userschema)
    def post(self,user_data):

        # user_data = request.get_json
        # error = Userschema()
        # err = error.validate(request.get_json)
        # if err:
        #     return jsonify({"status" : 401, "error " : err}),422
        user = UserModel(
                         name = user_data['name'],
                         email = user_data['email'],
                         password = pbkdf2_sha256.hash(user_data['password']),
                         phone_number = user_data['phone_number'],
                         role_id = user_data['role_id']                       
                         )
        try :
             db.session.add(user)
             db.session.commit()
        except IntegrityError:
             #abort(400,message="User  already Exists")
             return jsonify({"status": 400, "message": "User  already Exists" , "body":{}, "error" : {}}),400
             
        except SQLAlchemyError:
            #abort(500, mesage ="An Error Occured")
            return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {}})

        return user

        
    
@blp.route("/user/<string:user_id>")
class User(MethodView):
    @blp.response(200,Userschema)
    def get(self, user_id):
         user = UserModel.query.get_or_404(user_id)
         return user


    @blp.arguments(UserUpdateSchema)
    @blp.response(200,UserUpdateSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get(user_id)
        if user :
            user.name = user_data['name']
            user.email = user_data['email']
            user.phone_number = user_data['phone_number']
            user.role_id = user_data['role_id']
        else :
            user = UserModel(id=user_id,**user_data)

        db.session.add(user)
        db.session.commit()
        return user
        
    @jwt_required(fresh=True)
    def delete(self, user_id):
       user = UserModel.query.get_or_404(user_id)
       db.session.delete(user)
       db.session.commit()
       return {"mesage":"User deleted"}
    

@blp.route("/users/<int:page>")
class UserLis(MethodView):
    @blp.response(200,Userschema(many=True))
    def get(self,page):
        per_page= 5
        users = UserModel.query.paginate(page=page,per_page=per_page)
        # users['total_pages'] = 3
        # users['prev_page']=5
        # users['next_page']=5

        return users
    

@blp.route("/uk/")
class UserLis(MethodView):
    @blp.response(200,Userschema(many=True))
    def get(self):
        page = request.args.get('page',1,type=int)
        per_page= 5
        users = UserModel.query.paginate(page=page,per_page=per_page)
        # users['total_pages'] = 3
        # users['prev_page']=5
        # users['next_page']=5

        return users
    

@blp.route("/ff")
class Userfl(MethodView):
    #@blp.response(200,Userschema(many=True))
    def post(self):
        uploaded_file = request.files['file']
        fname = uploaded_file.filename
        fname = fname.replace(" ", "_")
        dice = os.path.join('uploads/',fname)
        uploaded_file.save(dice)
        #users = UserModel.query.paginate(page=page,per_page=per_page)
        # users['total_pages'] = 3
        # users['prev_page']=5
        # users['next_page']=5
        return {"message": "file uploaded","filename": fname}
        #return users

@blp.route("/loginapp")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    #@blp.response(UserLoginSchema)
    def post(self,user_data):
        user = UserModel.query.filter(UserModel.email == user_data['email']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password ):

            access_tocken = create_access_token(identity=user.id,fresh=True)
            refresh_access_token = create_refresh_token(identity=user.id)

            #return { "access_token": access_tocken}

            data = {
                "email": user.email,
                "id": user.id,
                "access_token": access_tocken,
                "refresh_access_token": refresh_access_token
            }
            return data
        #abort(401,message="Invalid Credntials" ,   body={})
        data = {"status": 401,"message" : "Invalid Credntials", "body":{}},401
        return data

@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(fresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        return { "access_token": new_token}
 

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jti()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Logout Successfully."}


@blp.route("/filter")
class Filters(MethodView):
    @blp.arguments(FilterSchema)
    @blp.response(200,ReviewSchema(many=True))
    def post(self,filter_data):
        search = filter_data['filter']
        searchs = "%{}%".format(search)
        brand  =  filter_data['brand']
        rbrand = "%{}%".format(brand)
        #user = UserModel.query.all()   #return all data in table
        ## user = UserModel.query.filter(UserModel.name.like(searchs)).all()    # like query
        #user = UserModel.query.filter(UserModel.name.like(searchs), UserModel.email.like(rbrand)).all() # And query

        user = ReviewModel.query.filter(or_(ReviewModel.brandname.like(searchs), ReviewModel.product.like(rbrand))).all() # or query
        #user = UserModel.query.filter(UserModel.role_id == "1").count()  #equal query with count only
        #user = UserModel.query.filter(UserModel.role_id == "1").all()    #equal query
        #user = UserModel.query.filter(UserModel.email == user_data['email']).first()  #equal query  with first item
        #users = user.all()
        return user
        # dd= {}
        # count=0
        # for use in user:
             
        #      dd['name'] = use.name
        #      count +1
        # return dd


@blp.route("/fileform")
class UserFiles(MethodView):
    @blp.arguments(FileformSchema)
    #@blp.response(200,Userschema(many=True))
    def post(self, user_data):
        
        uploaded_file = request.files['file']
        fname = uploaded_file.filename
        name = request.form['name']
        title = request.form['title']
        formdata = (name,title)
        data_dump = FileformSchema(many=True)
        data_dict = data_dump.dump(formdata)
        # if name  in request.form: 
        #     abort(500, mesage ="An Error Occured")
        # fname = fname.replace(" ", "_")
        # dice = os.path.join('uploads/',fname)
        # uploaded_file.save(dice)
        return {"message": "file uploaded","filename": fname,
                "name" : name , "title" : data_dict}
        #return users


@blp.route("/sendmail")
class SendEmail(MethodView):
    def get(self):
          msg = Message(
              subject = "Hi its test email",
              recipients= ["haroon.ssuet@gmail.com","haroonsaeed.ssuet@gmail.com"],
              sender= "haroon.ssuet@gmail.com"
              
          )
          msg.body="hello every one."
          #send_mail(msg)
          try: 
              mail.send(msg)
              return {"message" : "yessssssssssssss"}
          except Exception as e:
              print (e)
              return {"message" : f"mail not sent{e}"}
    
@blp.route("/supporter")
class GetSupporter(MethodView):
    @blp.arguments(SupporterSchema)
    @blp.response(200,Userschema(many=True))
    def get(self,user_data):
        followers = db.session.query(UserModel).join(SupporterModel,onclause=UserModel.id == SupporterModel.suppoter_id ).filter(SupporterModel.user_id == user_data["user_id"])
        #db.Query.join()
        # followers = (UserModel.select()
        #             .join(SupporterModel, on=SupporterModel.suppoter_id)
        #             .where(SupporterModel.user_id == user_data['user_id'])
        #             .order_by(UserModel.id))
        return followers
    

@blp.route("/add_supporter")
class AddSupporter(MethodView):
    @blp.arguments(SupporterSchema)
    def post(self,support_data):
        data = SupporterModel(**support_data)
        try :
            db.session.add(data)
            db.session.commit()

        except SQLAlchemyError :
            abort(500,message= "error")
        return {"message" : "Supporter Added"}
    
        
    

       

             
