from app.utils.dependencies import require_auth

from fastapi import APIRouter, Depends

router = APIRouter()

secret = "Passkeys are cool!"


@router.get("/")
async def get_secret(user=Depends(require_auth)):
    return {"secret": secret}
