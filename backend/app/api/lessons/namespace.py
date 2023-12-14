from flask_restx import Namespace

api = Namespace("lessons", description="Operations related to lessons")

from . import routes
