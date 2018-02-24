from flask_restplus import fields
from api.app import get_app

from model.user import User

app = get_app()

user_schema = app.api.model('User', {
    'id': fields.Integer(),
    'username': fields.String(),
    'fullname': fields.String(),
    'email': fields.String()
})

certificate_schema = app.api.model('Certificate', {
    'id': fields.Integer(),
    'name': fields.String(),
    'valid': fields.Boolean(),
    'user_id': fields.Integer()
})

profile_schema = app.api.model('Profile', {
    'id': fields.Integer(),
    'name': fields.String()
})

rule_schema = app.api.model('Rule', {
    'id': fields.Integer(),
    'name': fields.String(),
    'cidr': fields.String(),
    'proto': fields.String(),
    'port': fields.String(),
    'profile_id': fields.Integer()
})
