
import os
from flask import Flask,jsonify,redirect,url_for,session,make_response
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta

from db import db
from blocklist import BLOCKLIST
import models
from resources.user import blp as UserBlueprint
from resources.role import blp as RoleBlueprint
from resources.permission import blp as PermissionBlueprint
from resources.review import blp as ReviewBlueprint
from flask_mail  import Mail , Message
from authlib.integrations.flask_client import OAuth
from flask_migrate import Migrate

#mail =Mail()


def create_app(db_url=None):
    app = Flask(__name__)
    app.secret_key =" haroon saeed"

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "CRM REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "Haroon"

    app.config["MAIL_SERVER"] = "smtp.googlemail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = "haroon.ssuet@gmail.com"
    app.config["MAIL_PASSWORD"] = ""
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
   
    mail = Mail(app)
    # mail.init_app(app)


    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    #oath = OAuth(app)

    oath = OAuth()
    oath.init_app(app)

    google = oath.register(
            name = 'google',
            client_id = '',          
            client_secret='',
            access_token_url ='https://accounts.google.com/o/oauth2/token',
            access_token_params = None,
            authorize_url ='https://accounts.google.com/o/oauth2/auth',
            authorize_params = None,
            api_base_url = 'https://www.googleapis.com/oauth2/v1/',
            client_kwargs={'scope': 'openid profile email'},
            jwks_uri = "https://www.googleapis.com/oauth2/v3/certs"
            )
    
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoke_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message":"Token has been revoked.", "error" : "token_revoked"}),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return (
            jsonify({"message":"The token has expired.", "error":"expired_token"}),
            401,
            )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
               jsonify({"message":"Signature verification failed.", "error": "Invalid_token"}),
               401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"message":"Request does not contain an access token.", "error" : "authorization_required"}),
            401,
        )

    # with app.app_context():
    #     db.create_all()

    #@app.before_first_request()
    #def create_tables():
    #db.create_all()
    # @app.get("/test")
    # def get_stotes():
    #    return {"stores" : "test"}
    @app.errorhandler(404)
    def handle_404_error(_error):
        return make_response(jsonify({"status":404, "message":"404 error", "body" : {}, "error" : "Not Found Error"}),404)
    
    @app.errorhandler(422)
    def handle_422_error(_error):
        return make_response(jsonify({"status":422, "message":"422 error", "body" : {}, "error" : "Missing Error"}),422)
    

    @app.errorhandler(401)
    def handle_401_error(_error):
        return make_response(jsonify({"status":401, "message":"401 error", "body" : {}, "error" : "Bad Error"}),401)
    
    @app.errorhandler(500)
    def handle_500_error(_error):
        return make_response(jsonify({"status":500, "message":"500 error", "body" : {}, "error" : "server Error"}),500)
    
    @app.route("/sendemail")
    def sendemail():
          msg = Message(
              subject = "Hi its test email",
              recipients= [],
              sender= ""
              
          )
          msg.body="hello every one."
          try: 
              mail.send(msg)
              return {"message" : "hi"}
          except Exception as e:
              print (e)
              return {"message" : f"mail not sent{e}"}
    
    @app.route("/login")
    def login():
        google = oath.create_client('google')
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri)

    @app.route("/authorize")
    def authorize():
        google = oath.create_client('google')
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        resp.raise_for_status()
        user_info = resp.json()
        # do something with the token and profile
       # session['email'] = user_info['email']
        return jsonify(user_info)
        return redirect('/')
    # @app.route("/")
    # def hello_world():
    #     #print(session['email'])
    #     email = session['email'] 
    #     return f'hello, {email}'
    

    @app.route("/logoutt")
    def google_logoutt():
        return {"logoutt": "logoutt"}
    
    def send_mai(msg):
        try: 
              mail.send(msg)
              return {"message" : "hi"}
        except Exception as e:
              print (e)
              return {"message" : f"mail not sent{e}"}





    api.register_blueprint(UserBlueprint)
    api.register_blueprint(RoleBlueprint)
    api.register_blueprint(PermissionBlueprint)
    api.register_blueprint(ReviewBlueprint)

    return app




