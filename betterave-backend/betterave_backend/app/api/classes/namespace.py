from flask_restx import Namespace

api = Namespace("classes", description="Class related operations")

from . import routes
