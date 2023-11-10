from flask_restx import fields
from .namespace import api

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
})

login_status_model = api.model('LoginStatus', {
    'status': fields.String(description='Authentication status'),
    'role': fields.String(description='Type of user if authenticated'),
})
