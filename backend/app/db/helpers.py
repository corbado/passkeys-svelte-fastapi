from typing import Optional

from sqlalchemy.orm import Session

from .models import User


def get_user(db: Session, user_id: str) -> Optional[User]:
    """
    Fetch a user from the database by corbado_user_id.
    """
    return db.query(User).filter(User.corbado_user_id == user_id).first()



def insert_user(db: Session, user_id: str) -> User:
    """
    Insert a new user into the database.
    """
    new_user = User(corbado_user_id=user_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user_city(db: Session, corbado_user_id: str, city: str) -> Optional[User]:
    """
    Update a user's city given their Corbado user ID.
    Returns the updated User object if found, otherwise None.
    """
    user = db.query(User).filter(User.corbado_user_id == corbado_user_id).first()
    if user:
        user.city = city
        db.commit()
        db.refresh(user)
        return user
    return None
