# type: ignore
"""Custom decorators for Flask routes.

with_instance:
    Decorator factory that accepts a single SQLAlchemy model class or a list of them.
    The resulting decorator converts IDs to instances for the specified leading arguments,

    Example:

    def get_user_name(user_id: int):
        user = User.query.get(user_id)
        return user.name

    Becomes:

    @with_instance(User)
    def get_user_name(user: User):
        return user.name

    >> get_user_name(user_id=1)

require_authentication:
    A decorator that requires authentication for a Flask route. If the user is not authenticated, the decorator
    will check for a valid API key in the request headers. If the user is authenticated, the decorator will check
    if the user has the required user type(s) to access the route.

    If no user types are specified, the decorator will allow any authenticated user to access the route.

current_user_required:
    Decorator that ensures the current user is authenticated and is either the user specified by the user_id
    in the route or an admin. If the API key is provided, it also validates the key.

resolve_user:
    Decorator that resolves the user from the user_id_or_me parameter in the route. If the user_id_or_me parameter
    is "me", the current user is used. Otherwise, the user is resolved from the user_id_or_me parameter.
"""

import os
from typing import Any, Callable, List, Type, Union
from functools import wraps
from backend.extensions import db
from flask_login import current_user
from flask import jsonify, request
from flask_restx import abort
from backend.app.models import User


def is_valid_apikey(key: str) -> bool:
    """Check if the API key is valid."""
    return key == os.getenv("API_KEY")


def with_instance(model_classes: Union[Type[Any], List[Type[Any]]]) -> Callable:
    """
    Convert IDs to instances through a decorator factory.

    It accepts a single SQLAlchemy model class or a list of them.
    The resulting decorator converts IDs to instances for the specified leading arguments,

    Example:

    def get_user_name(user_id: int):
        user = User.query.get(user_id)
        return user.name

    Becomes:

    @with_instance(User)
    def get_user_name(user: User):
        return user.name

    >> get_user_name(user_id=1)
    """
    if not isinstance(model_classes, list):
        model_classes = [model_classes]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) < len(model_classes):
                raise ValueError("Not enough arguments provided to match the model classes.")

            new_args = list(args)  # Convert args to a list to allow modifications
            for i, model_class in enumerate(model_classes):
                arg = args[i]
                if isinstance(arg, int):
                    instance = db.session.get(model_class, arg)
                    if instance is None:
                        raise ValueError(f"{model_class.__name__} with ID {arg} not found.")
                    new_args[i] = instance
                elif not isinstance(arg, model_class):
                    raise ValueError(
                        f"Argument at position {i} must be an instance of {model_class.__name__} or an integer ID."
                    )

            return func(*new_args, **kwargs)

        return wrapper

    return decorator


def require_authentication(*user_types_required: List[str]):
    """
    Authentificate user or check for valid API key.

    If the user is authenticated, the decorator will check if the user
    has the required user type(s) to access the route.
    If no user types are specified, the decorator will allow any authenticated user to access the route.
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Skip API key check if the user is already authenticated
            if not current_user.is_authenticated:
                apikey = request.headers.get("X-API-KEY")
                if not apikey or not is_valid_apikey(apikey):
                    abort(401, "Invalid or missing API key")

            # Check user type only if user is authenticated
            if current_user.is_authenticated:
                if not hasattr(current_user, "user_type"):
                    abort(500, "Unable to determine user type")
                if len(user_types_required) > 0 and (current_user.user_type.value not in user_types_required):
                    allowed_types = ", ".join(user_types_required)
                    abort(
                        403,
                        f"You must be one of the following types to perform this action: {allowed_types}",
                    )
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def current_user_required(f: Callable) -> Callable:
    """
    Ensure that the current user is either the user specified by the user_id in the route or an admin.

    If the API key is provided, it also validates the key.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Flask passes the URL parameters as keyword arguments to the decorated function
        user = kwargs.get("user", None)

        # If the current user is authenticated through Flask-Login's current_user
        if current_user.is_authenticated:
            # Allow admins or if user_id matches the current_user's id
            if current_user.is_admin or (user.user_id == current_user.user_id):
                return f(*args, **kwargs)
            else:
                abort(403, "You do not have permission to access this resource.")

        # If not authenticated, check for API key
        apikey = request.headers.get("X-API-KEY")
        if apikey and is_valid_apikey(apikey):
            # If valid API key, proceed without checking user_id against current_user
            return f(*args, **kwargs)

        # If neither authenticated nor valid API key provided, deny access
        abort(401, "Unauthorized access")

    return decorated_function


def resolve_user(f: Callable) -> Callable:
    """
    Resolve the user from the user_id_or_me parameter in the route.

    If the user_id_or_me parameter is "me", the current user is used.
    Otherwise, the user is resolved from the user_id_or_me parameter.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id_or_me = kwargs.get("user_id_or_me", None)
        if not user_id_or_me:
            return jsonify({"message": "User ID not specified:"}), 400
        if user_id_or_me == "me":
            # Assuming "current_user" is a proxy to the current user
            user = current_user
        else:
            user = User.query.get(int(user_id_or_me))
            if not user:
                return jsonify({"message": "User not found"}), 404
        # Replace "user_id_or_me" with "user" before calling the actual route function
        kwargs["user"] = user
        # Remove "user_id" to match the expected parameters of the actual route function
        kwargs.pop("user_id_or_me", None)
        return f(*args, **kwargs)

    return decorated_function
