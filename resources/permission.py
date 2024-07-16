import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PermissionSchema
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import PermissionModel

#from db import role,role_permission

blp = Blueprint("permission", __name__,description="Operation on role")

@blp.route("/permissions")
class RoleList(MethodView):
    # @blp.response(200,RoleSchema(many=True))
    # def get(self):
    #     return role.values()
    @blp.arguments(PermissionSchema)
    @blp.response(200,PermissionSchema)
    def post(self, permission_data):
        #roles = role_data['name']
        permission =  PermissionModel(**permission_data)
        try:
            db.session.add(permission)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message =" an occur")

        return permission



# @blp.route("/role/<string:role_id>")
# class Role(MethodView):
#     @blp.response(200,RoleSchema)
#     def get(self, role_id):
#         get_role = role[role_id]
#         get_role_permission = role_permission[role_id]
#         get_permission = get_role_permission
#         get_permission['name'] = get_role['name']
#         return get_permission
    
#     @blp.arguments(RoleUpdateSchema)
#     @blp.response(200,RoleUpdateSchema)
#     def put(self, role_data, role_id):
#         #role_date = request.get_json()
#         gt_role  = role[role_id]
#         gt_role['name'] = role_data['name']
#         return gt_role
    
#     def delete(self, role_id):
#         del role[role_id]
#         del role_permission[role_id]
#         return { "message ": "role deleetd successfully"}
