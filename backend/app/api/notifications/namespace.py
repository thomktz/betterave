from flask_restx import Namespace

api = Namespace("notifications", description="Notification related operations")

from . import routes
