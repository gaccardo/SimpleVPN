import os
import tempfile
import shutil

from flask import request, send_file
from flask_restplus import Resource, fields, marshal, errors

from api.app import get_app
from api.resources.schema import user_schema, certificate_schema
from model.user import User as DBUser
from model.certificate import Certificate as DBCertificate

from api.tools.openvpn import generate_client_config


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
        except e:
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
        for k, v in request.json.iteritems():
            setattr(user, k, v)
        app.db.session.merge(user)
        app.db.session.commit()
        return marshal(user, user_schema), 200


@ns.route('/<int:id>/certificates')
class CertificatesByUser(Resource):

    @ns.doc('list certificates by user')
    @app.api.marshal_with(certificate_schema, as_list=True)
    def get(self, id):
        certificates = app.db.session.query(DBCertificate).filter(
            DBCertificate.user_id == id
        ).all()
        return marshal(certificates, certificate_schema), 200


@ns.route('/<int:id>/certificate/<int:certificate_id>/download')
class DownloadCertificate(Resource):

    @ns.doc('download certificates by user')
    @app.api.doc(
        responses={
            200: 'Success',
            404: 'Certificate Not Found',
            409: 'Certificate Is Revoked'
        }
    )
    def get(self, id, certificate_id):
        certificate = app.db.session.query(DBCertificate).filter(
            DBCertificate.id == certificate_id
        ).first()
        if certificate is None:
            errors.abort(code=404, message="Certicate Not Found")

        if not certificate.valid:
            errors.abort(code=409, message="Certicate is Revoked")

        temorary_certificates_folder = tempfile.mkdtemp(dir="/tmp")
        files_to_copy = [
            "/etc/openvpn/keys/{}.crt".format(certificate.name),
            "/etc/openvpn/keys/{}.key".format(certificate.name),
            "/etc/openvpn/keys/ca.crt"
        ]
        for ff in files_to_copy:
            shutil.copy2(ff, temorary_certificates_folder)

        generate_client_config(certificate.name, temorary_certificates_folder)
        shutil.make_archive(
            "/tmp/{}".format(certificate.name),
            "zip",
            temorary_certificates_folder
        )
        shutil.rmtree(temorary_certificates_folder)
        return send_file(
            "/tmp/{}.zip".format(certificate.name),
            attachment_filename='{}.zip'.format(certificate.name),
            as_attachment=True
        )


@ns.route('/<int:id>/certificate/<int:certificate_id>/send')
class SendCertificate(Resource):

    @ns.doc('send certificate to user')
    def get(self, id, certificate_id):
        certificate = app.db.session.query(DBCertificate).filter(
            DBCertificate.id == certificate_id
        ).first()
        temorary_certificates_folder = tempfile.mkdtemp(dir="/tmp")
        files_to_copy = [
            "/etc/openvpn/keys/{}.crt".format(certificate.name),
            "/etc/openvpn/keys/{}.key".format(certificate.name),
            "/etc/openvpn/keys/ca.crt"
        ]
        for ff in files_to_copy:
            shutil.copy2(ff, temorary_certificates_folder)

        generate_client_config(certificate.name, temorary_certificates_folder)
        shutil.make_archive(
            "/tmp/{}".format(certificate.name),
            "zip",
            temorary_certificates_folder
        )
        shutil.rmtree(temorary_certificates_folder)
        # send to user
