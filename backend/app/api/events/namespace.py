from flask_restx import Namespace

api = Namespace('events', description='Event related operations')

from . import routes