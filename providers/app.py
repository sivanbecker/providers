import os
from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime, date
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


providers = [
    {
        'id': 1,
        'mispar_osek': '024984064',
        'name': 'Bosmat Baruch',
        'service_type': 'Ripui Be Isuk',
        'added': date(day=13, month=10, year=2020),
     },
]


POSTGRES_URL = os.environ.get("POSTGRES_URL")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PW = os.environ.get("POSTGRES_PW")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)

class ProviderSchema(ma.Schema):
    class Meta:
        fields = ("name", "mispar_osek", "service_type", "added")

provider_schema = ProviderSchema()
providers_schema = ProviderSchema(many=True)

## DB
class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mispar_osek = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    service_type = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'<Provider {self.name} - {self.mispar_osek}>'

db.create_all()

## Routes



class ProviderListResource(Resource):
    def get(self):
        return {'providers': providers_schema.dump(Provider.query.all())}


class ProviderResource(Resource):

    def get(self, mispar_osek):
        try:
            _provider = Provider.query.filter_by(mispar_osek=mispar_osek).one()
            return {'provider': provider_schema.dump(_provider)}
        except NoResultFound:
            return {'provider': None}, 404

    def post(self, mispar_osek):
        if Provider.query.filter_by(mispar_osek=mispar_osek).count():
            return {'message': 'Provider with mispar-osek={mispar_osek} already exists'}, 400

        data = request.get_json()
        new_provider = Provider(
            name=data['name'],
            mispar_osek=mispar_osek,
            service_type=data['service_type'],
            added=datetime.now()
        )
        try:
            db.session.add(new_provider)
            db.session.commit()
            return {'provider': provider_schema.dump(new_provider)}
        except IntegrityError as e:
            return {'message': str(e)}



    def put(self, mispar_osek):
        data = request.get_json()
        try:
            _provider = Provider.query.filter_by(mispar_osek=mispar_osek).one()
            _provider.service_type = data['service_type']
            _provider.name = data['name']
            return {'message': 'Provider updated'}
        except NoResultFound:
            new_provider = Provider(
                name=data['name'],
                mispar_osek=mispar_osek,
                service_type=data['service_type'],
                added=datetime.now()
            )
            db.session.add(new_provider)
            db.session.commit()
            return {'provider': provider_schema.dump(new_provider)}, 201

    def delete(self, mispar_osek):
        try:
            _provider = Provider.query.filter_by(mispar_osek=mispar_osek).one()
            db.session.delete(_provider)
            db.session.commit()
            return {'message': 'Provider Deleted'}
        except NoResultFound:
            return {'message': f'Provider with mispar-osek={mispar_osek} does not exist'}, 400


api.add_resource(ProviderResource, '/provider/<string:mispar_osek>')
api.add_resource(ProviderListResource, '/providers')

app.run(port=5000, debug=True)
