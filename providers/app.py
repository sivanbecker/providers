import os
from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime, date
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

#from models.provider import Provider
from resources.provider import ProviderResource, ProviderListResource
#from resources.provider_list import ProviderListResource

POSTGRES_URL = os.environ.get("POSTGRES_URL")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PW = os.environ.get("POSTGRES_PW")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
#db = SQLAlchemy(app)
api = Api(app)

api.add_resource(ProviderResource, '/provider/<string:mispar_osek>')
api.add_resource(ProviderListResource, '/providers')

if __name__ == "__main__":
    from db import db
    from schemas.provider import ma
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5001, host='0.0.0.0', debug=True)
