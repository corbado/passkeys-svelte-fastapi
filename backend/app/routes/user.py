from app.db.db import get_db
from app.db.helpers import get_user, insert_user, update_user_city
from app.utils.authentication import get_user_identifiers
from app.utils.dependencies import require_auth
from corbado_python_sdk import UserEntity
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def info(user: UserEntity = Depends(require_auth), db: Session = Depends(get_db)):
    user_id = user.user_id

    db_user = get_user(db, user_id)
    if not db_user:
        db_user = insert_user(db, user_id)

    user_identifiers = get_user_identifiers(user_id)

    # Return JSON response
    return {
        "user": {
            "id": db_user.id,
            "corbado_user_id": db_user.corbado_user_id,
            "city": db_user.city,
            "created_at": db_user.created_at,
            "updated_at": db_user.updated_at,
        },
        "identifiers": user_identifiers.identifiers
    }



@router.post("/city")
async def update_city(request: Request, user: UserEntity = Depends(require_auth), db: Session = Depends(get_db)):
    # Parse body to get city
    body = await request.json()
    city = body.get("city")
    if city is None:
        # If there's no 'city' in the request body, handle accordingly
        raise HTTPException(
            status_code=400,
            detail="Missing 'city' field in request body."
        )

    # Update user's city in the database
    update_user_city(db, user.user_id, city)

    # Fetch the updated user
    updated_user = get_user(db, user.user_id)

    # Return the updated user as JSON
    return {
        "id": updated_user.id,
        "corbado_user_id": updated_user.corbado_user_id,
        "city": updated_user.city,
        "created_at": updated_user.created_at,
        "updated_at": updated_user.updated_at
    }
