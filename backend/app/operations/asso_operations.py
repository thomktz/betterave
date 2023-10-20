from extensions import db
from app.models.user import User, UserType
from app.operations.user_operations import get_user_by_id
from sqlalchemy.exc import SQLAlchemyError

def subscribe_to_asso(user_id: int, asso_id: int) -> bool:
    try:
        user = get_user_by_id(user_id)
        asso = get_user_by_id(asso_id)
        
        if not user or not asso:
            return False

        # If already subscribed, no need to proceed
        if asso in user.subscriptions:
            return True
        
        user.subscriptions.append(asso)
        db.session.commit()
        return True

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error subscribing user to asso: {str(e)}")
        return False

def unsubscribe_from_asso(user_id: int, asso_id: int) -> bool:
    try:
        user = get_user_by_id(user_id)
        asso = get_user_by_id(asso_id)
        
        if not user or not asso:
            return False

        # If not subscribed, no need to proceed
        if asso not in user.subscriptions:
            return True
        
        user.subscriptions.remove(asso)
        db.session.commit()
        return True

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error unsubscribing user from asso: {str(e)}")
        return False

def get_all_assos():
    """Get all associations."""
    return User.query.filter_by(user_type=UserType("asso")).all()