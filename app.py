import os
from flask import Flask
from flask_smorest import Api
from flask_uploads import configure_uploads
from db import db 
from resources.acquisition import blp as AcquisitionBlueprint
from resources.patient import blp as PatientBlueprint
from image_helper import IMAGE_SET



def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "RetiSpec POC REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
    app.config["UPLOADED_IMAGES_DEST"] = os.path.join("static", "images")  
    configure_uploads(app, IMAGE_SET)
    db.init_app(app)
    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(AcquisitionBlueprint)
    api.register_blueprint(PatientBlueprint)


    return app