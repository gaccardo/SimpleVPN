from flask import request
from flask_restplus import Resource, fields, marshal, errors

from api.app import get_app

from api.resources.schema import profile_schema
from model.profile import Profile as DBProfile
from api.resources.schema import rule_schema
from model.rule import Rule as DBRule


app = get_app()
ns = app.api.namespace('profile',
                       description='Profile operations')


@ns.route('')
class ProfileList(Resource):

    @ns.doc('list profiles')
    @app.api.marshal_with(profile_schema, as_list=True)
    def get(self):
        profiles = app.db.session.query(DBProfile).all()
        return marshal(profiles, profile_schema), 200

    @ns.doc('post profile')
    @app.api.expect(profile_schema, validate=True)
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found',
            409: 'Profile Already Exists'
        }
    )
    def post(self):
        new_profile = DBProfile(**request.json)
        app.db.session.add(new_profile)
        try:
            app.db.session.commit()
        except, e:
            errors.abort(code=409, message="Profiles alredy exists")
        return 200


@ns.route('/<int:id>')
class Profile(Resource):

    @ns.doc('list profiles')
    @app.api.marshal_with(profile_schema)
    def get(self, id):
        profile = app.db.session.query(DBProfile).get(id)
        if profile is None:
            errors.abort(code=404, message="Profile Not Found")
        return marshal(profile, profile_schema), 200

    @ns.doc('delete profile')
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found',
        }
    )
    def delete(self, id):
        profile = app.db.session.query(DBProfile).get(id)
        if profile is None:
            errors.abort(code=404, message="Profile Not Found")
        app.db.session.delete(profile)
        app.db.session.commit()
        return 200

    @ns.doc('update profile')
    @app.api.marshal_with(profile_schema)
    @app.api.expect(profile_schema, validate=True)
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found',
        }
    )
    def put(self, id):
        profile = app.db.session.query(DBProfile).get(id)
        if profile is None:
            errors.abort(code=404, message="Profile Not Found")
        for k, v in request.json.iteritems():
            setattr(profile, k, v)
        app.db.session.merge(profile)
        app.db.session.commit()
        return marshal(profile, profile_schema), 200


@ns.route('/<int:id>/rule')
class RuleByProfile(Resource):

    @ns.doc('list rules by profile')
    @app.api.marshal_with(rule_schema, as_list=True)
    def get(self, id):
        rules = app.db.session.query(DBRule).filter(
            DBRule.profile_id == id
        ).all()
        return marshal(rules, rule_schema), 200
