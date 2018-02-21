from flask import request
from flask_restplus import Resource, fields, marshal, errors

from api.app import get_app

from api.resources.schema import user_schema
from model.user import User as DBUser

app = get_app()
ns = app.api.namespace('user', description='User operations')


@ns.route('')
class UserList(Resource):

    @ns.doc('list users')
    @app.api.marshal_with(user_schema, as_list=True)
    def get(self):
        users = app.db.session.query(DBUser).all()
        return marshal(users, user_schema), 200


    @ns.doc('post user')
    @app.api.expect(user_schema, validate=True)
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found',
            409: 'Conflict',
            500: 'Internal Server Error'
        }
    )
    def post(self):
        new_user = DBUser(**request.json)
        app.db.session.add(new_user)

        try:
            app.db.session.commit()
        except:
            errors.abort(code=409, message="User already exists")
        return 200


@ns.route('/<int:id>')
class User(Resource):

    @ns.doc('get user')
    @app.api.marshal_with(user_schema)
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found'
        }
    )
    def get(self, id):
        user = app.db.session.query(DBUser).get(id)
        if not user:
            errors.abort(code=404, message="User not found")
        return marshal(user, user_schema), 200

    @ns.doc('delete user')
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found'
        }
    )
    def delete(self, id):
        user = app.db.session.query(DBUser).get(id)
        if not user:
            errors.abort(code=404, message="User not found")
        app.db.session.delete(user)
        app.db.session.commit()
        return {'msg': 'user deleted'}

    @ns.doc('update user')
    @app.api.marshal_with(user_schema)
    @app.api.expect(user_schema, validate=True)
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found'
        }
    )
    def put(self, id):
        user = app.db.session.query(DBUser).get(id)
        if not user:
            errors.abort(code=404, message="User not found")
        for k,v in request.json.iteritems():
            setattr(user, k, v)
        app.db.session.merge(user)
        app.db.session.commit()
        return marshal(user, user_schema), 200
