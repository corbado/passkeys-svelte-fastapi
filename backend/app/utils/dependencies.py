from fastapi import HTTPException, Request
from corbado_python_sdk import UserEntity


def require_auth(request: Request) -> UserEntity:
    user = getattr(request.state, "corbado_user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
