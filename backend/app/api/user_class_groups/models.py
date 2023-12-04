from flask_restx import fields
from .namespace import api

user_class_group_model = api.model(
    "UserClassGroup",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the user-class group relationship",
        ),
        "user_id": fields.Integer(required=True, description="Identifier of the user"),
        "class_id": fields.Integer(required=True, description="Identifier of the class"),
        "primary_class_group_id": fields.Integer(description="Identifier of the primary class group"),
        "secondary_class_group_id": fields.Integer(description="Identifier of the secondary class group"),
    },
)

user_class_group_update_model = api.model(
    "UpdateUserClassGroup",
    {
        "secondary_class_group_name": fields.String(
            required=True,
            description="The new name of the secondary class group to associate with the user-class group",
        )
    },
)
