import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,get_jwt_identity
from schemas import RoleSchema, RoleUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import RoleModel

#from db import role,role_permission

blp = Blueprint("role", __name__,description="Operation on role")

@blp.route("/role")
class RoleList(MethodView):
    @blp.response(200,RoleSchema(many=True))
    def get(self):
        roles = RoleModel.query.all()
        return roles
    
    #@jwt_required()
    @blp.arguments(RoleSchema)
    @blp.response(200,RoleSchema)
    def post(self, role_data):
        #jwt = get_jwt_identity()
        #idd = jwt.get_jwt_identity()
        # if jwt == 2 :
        #     abort(401, message= "hello")
        
        # abort(401, message = "2")
        #role =  RoleModel(**role_data)
        role  = RoleModel(
                           name = role_data['name'],
                           status = "1"
         )
        try:
            db.session.add(role)
            db.session.commit()
        except IntegrityError:
            abort(500 ,message ="Role Already Exsists.")
        except SQLAlchemyError:
            abort(500,message ="An error occur.")

        return role

@blp.route("/role/<string:role_id>")
class Role(MethodView):
    @blp.response(200,RoleSchema)
    def get(self, role_id):
        role = RoleModel.query.get_or_404(role_id)
        return role
    
    @blp.arguments(RoleUpdateSchema)
    @blp.response(200,RoleUpdateSchema)
    def put(self, role_data, role_id):
        role = RoleModel.query.get(role_id)
        if role:
            role.name = role_data['name']
        else :
            role = RoleModel(id=role_id,**role_data)
        
        db.session.add(role)
        db.session.commit()
        return role
    
    def delete(self, role_id):
        role = RoleModel.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        return {"message": "Role Deleted"}
