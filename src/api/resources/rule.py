from flask import request
from flask_restplus import Resource, fields, marshal, errors

from api.app import get_app

from api.resources.schema import rule_schema
from model.rule import Rule as DBRule
from model.profile import Profile as DBProfile
from api.tools import iptables


app = get_app()
ns = app.api.namespace('rule',
                       description='Rule operations')


@ns.route('')
class RuleList(Resource):

    @ns.doc('list rules')
    @app.api.marshal_with(rule_schema, as_list=True)
    def get(self):
        rules = app.db.session.query(DBRule).all()
        return marshal(rules, rule_schema), 200

    @ns.doc('post rule')
    @app.api.expect(rule_schema, validate=True)
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found',
            409: 'Rule Already Exists'
        }
    )
    def post(self):
        new_rule = DBRule(**request.json)
        profile = app.db.session.query(DBProfile).filter(
            DBProfile.id == request.json['profile_id']
        ).first()
        if profile is None:
            errors.abort(code=404, message="Profile Not Found")
        app.db.session.add(new_rule)
        try:
            app.db.session.commit()
        except:
            errors.abort(code=409, message="Rule alredy exists")
        return 200


@ns.route('/<int:id>')
class Rule(Resource):

    @ns.doc('get rule')
    @app.api.marshal_with(rule_schema)
    def get(self, id):
        rule = app.db.session.query(DBRule).get(id)
        if rule is None:
            errors.abort(code=404, message="Rule Not Found")
        return marshal(rule, rule_schema), 200

    @ns.doc('delete rule')
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found',
        }
    )
    def delete(self, id):
        rule = app.db.session.query(DBRule).get(id)
        if rule is None:
            errors.abort(code=404, message="Rule Not Found")
        app.db.session.delete(rule)
        app.db.session.commit()
        return 200

    @ns.doc('update rule')
    @app.api.marshal_with(rule_schema)
    @app.api.expect(rule_schema, validate=True)
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found',
        }
    )
    def put(self, id):
        rule = app.db.session.query(DBRule).get(id)
        if profile is None:
            errors.abort(code=404, message="Rule Not Found")
        for k, v in request.json.iteritems():
            setattr(rule, k, v)
        app.db.session.merge(rule)
        app.db.session.commit()
        return marshal(rule, rule_schema), 200


@ns.route('/apply')
class RuleApply(Resource):

    @ns.doc('applu rules')
    def post(self):
        iptables.apply_rules(app.db.session)
        return 200
