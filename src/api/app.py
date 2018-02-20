from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api


import settings

app = Flask(__name__)
app.config.from_object(settings)
app.debug = settings.DEBUG
app.db = SQLAlchemy(app)
app.api = Api(app, version='v1')
blueprint = Blueprint('simplevpn', __name__)
app.api.init_app(blueprint)
app.register_blueprint(blueprint)


def get_app():
    global app
    return app
