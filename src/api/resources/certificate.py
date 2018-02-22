from flask import request
from flask_restplus import Resource, fields, marshal, errors

from api.app import get_app

from api.resources.schema import certificate_schema, user_schema
from model.certificate import Certificate as DBCertificate
from model.user import User as DBUser
from api.tools import openvpn


app = get_app()
ns = app.api.namespace('certificate',
                       description='Certificate operations')


@ns.route('')
class CertificateList(Resource):

    @ns.doc('list users')
    @app.api.marshal_with(certificate_schema, as_list=True)
    def get(self):
        certificates = app.db.session.query(DBCertificate).all()
        return marshal(certificates, certificate_schema), 200

    @ns.doc('post certificate')
    @app.api.expect(certificate_schema, validate=True)
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found',
            409: 'Already Exists',
            500: 'Internal Server Error'
        }
    )
    def post(self):
        if openvpn.generate_certificate(request.json):
            new_certificate = DBCertificate(**request.json)
            app.db.session.add(new_certificate)
            try:
                app.db.session.commit()
            except e:
                errors.abort(code=409, message="Certificate already exists")
        else:
            errors.abort(code=500, message="Error creating the certificate")

        return marshal(new_certificate, certificate_schema), 200


@ns.route('/<int:id>')
class Certificate(Resource):

    @ns.doc('get certificate')
    @app.api.marshal_with(certificate_schema)
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found'
        }
    )
    def get(self, id):
        certificate = app.db.session.query(DBCertificate).get(id)
        if certificate is None:
            errors.abort(code=404, message="Certificate not found")
        return marshal(certificate, certificate_schema), 200

    @ns.doc('revoke certificate')
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Not Found',
            409: 'Certificate already revoked'
        }
    )
    def delete(self, id):
        certificate = app.db.session.query(DBCertificate).get(id)
        if certificate is None:
            errors.abort(code=404, message="Certificate not found")
        if not certificate.valid:
            errors.abort(code=409, message="Certificate already revoked")
        certificate.valid = False
        app.db.session.merge(certificate)
        app.db.session.commit()
        return 200


@ns.route('/user/<int:user_id>')
class CertificateUser(Resource):

    @ns.doc('list users')
    @app.api.marshal_with(certificate_schema, as_list=True)
    @app.api.doc(
        responses={
            200: 'Success'
        }
    )
    def get(self, user_id):
        certificates = app.db.session.query(DBCertificate).filter(
            DBCertificate.user_id == user_id
        ).all()
        return marshal(certificates, certificate_schema), 200
