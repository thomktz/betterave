from flask_restx import Namespace

api = Namespace('auth', description='Authentication related operations')

from . import routes