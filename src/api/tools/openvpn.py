import os

from mako.template import Template

from api.app import get_app


def generate_certificate(certificate_data):
    return True


def generate_client_config(certificate, dst_folder):
    app = get_app()
    template_file = os.path.join(app.root_path, 'tools', 'templates',
                                 'client.conf')
    client_template = Template(filename=template_file)
    config = client_template.render(certificate=certificate,
                                    server_ip="127.0.0.1")
    config_file_path = os.path.join(dst_folder, 'client.conf')
    with open(config_file_path, 'w') as config_file:
        config_file.write(config)
