from flask_restx import Namespace

api = Namespace('users', description='User related operations')

from . import routes
