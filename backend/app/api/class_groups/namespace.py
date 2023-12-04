from flask_restx import Namespace

api = Namespace("class_groups", description="Operations related to class groups")

from . import routes