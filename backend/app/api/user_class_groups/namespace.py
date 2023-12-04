from flask_restx import Namespace

api = Namespace("user_class_groups", description="Operations related to user class groups")

from . import routes