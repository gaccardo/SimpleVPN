from flask import request
from flask_restplus import Resource, fields, marshal, errors

from api.app import get_app

from api.resources.schema import user_schema
from model.user import User

app = get_app()
ns = app.api.namespace('user', description='User operations')


@ns.route('')
class UserList(Resource):

    @ns.doc('list users')
    @app.api.marshal_with(user_schema, as_list=True)
    def get(self):
        users = app.db.session.query(User).all()
        return marshal(users, user_schema), 200
