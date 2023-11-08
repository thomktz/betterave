from typing import Any, Callable, List, Type, Union
from functools import wraps
from extensions import db
from flask_login import current_user
from flask import jsonify


def with_instance(model_classes: Union[Type[Any], List[Type[Any]]]) -> Callable:
    """
    Decorator factory that accepts a single SQLAlchemy model class or a list of them.
    The resulting decorator converts IDs to instances for the specified leading arguments,
    allowing the function to accept a mix of instances and IDs for those arguments.
    Other arguments are passed through unchanged.
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
                    raise ValueError(f"Argument at position {i} must be an instance of {model_class.__name__} or an integer ID.")

            return func(*new_args, **kwargs)
        return wrapper
    return decorator


def type_required(*user_types_required):
    """Decorator to check if the current user is authenticated and has the required user type."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("Current user in type_required is", current_user)
            if not current_user.is_authenticated:
                return jsonify({'message': 'Authentication is required'}), 401

            if not hasattr(current_user, 'user_type'):
                return jsonify({'message': 'Unable to determine user type'}), 500

            if current_user.user_type.value not in user_types_required:
                allowed_types = ', '.join(user_types_required)
                return jsonify({'message': f'You must be one of the following types to perform this action: {allowed_types}'}), 403
            print("User type is correct")
            return f(*args, **kwargs)
        return decorated_function
    return decorator