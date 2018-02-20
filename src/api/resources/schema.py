from flask_restplus import fields
from api.app import get_app

from model.user import User

app = get_app()

user_schema = app.api.model('User', {
    'id': fields.Integer(),
    'username': fields.String(),
    'fullname': fields.String(),
    'email': fields.String(),
    'certificate': fields.String()
})
