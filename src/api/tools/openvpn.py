import os

from mako.template import Template
from flask_restplus import errors

from api.app import get_app
from model.user import User as DBUser
from model.certificate import Certificate as DBCertificate

app = get_app()


def certificate_exists(certificate_data):
    certificate = app.db.session.query(DBCertificate).filter(
        DBCertificate.name == certificate_data['name']
    ).first()
    return certificate is not None


def generate_certificate(certificate_data):
    user = app.db.session.query(DBUser).get(certificate_data['user_id'])

    if user is None:
        errors.abort(code=404, message="User not found")

    if certificate_exists(certificate_data):
        errors.abort(code=409, message="Certificate already exists")

    # KEY_CONFIG /etc/openvpn/openvpn-ca/openssl-1.0.0.cnf
    # KEY_DIR /etc/openvpn/openvpn-ca/

    # THIS IS UGLY, IMPROVE IT
    helper_path = os.path.join(app.root_path, 'tools', 'openvpn.sh')
    os.system("{} {}".format(helper_path, certificate_data['name']))

    return False


def generate_client_config(certificate, dst_folder):
    template_file = os.path.join(app.root_path, 'tools', 'templates',
                                 'client.conf')
    client_template = Template(filename=template_file)
    config = client_template.render(certificate=certificate,
                                    server_ip="127.0.0.1")
    config_file_path = os.path.join(dst_folder, 'client.conf')
    with open(config_file_path, 'w') as config_file:
        config_file.write(config)
