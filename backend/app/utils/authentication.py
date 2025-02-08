from typing import Optional

from app.core.config import Config as Settings
import os
from corbado_python_sdk.generated.models import IdentifierList
from corbado_python_sdk import Config, CorbadoSDK, UserEntity

config = Config(
    project_id=os.environ.get('CORBADO_PROJECT_ID'),
    api_secret=os.environ.get('CORBADO_API_SECRET'),
    frontend_api=os.environ.get('CORBADO_FRONTEND_API'),
    backend_api=os.environ.get('CORBADO_BACKEND_API')
)
sdk = CorbadoSDK(config=config)


config = Config(
    project_id=Settings.CORBADO_PROJECT_ID,
    api_secret=Settings.CORBADO_API_SECRET,
    frontend_api=Settings.CORBADO_FRONTEND_API,
    backend_api=Settings.CORBADO_BACKEND_API
)
sdk = CorbadoSDK(config=config)


from fastapi import Request


def get_authenticated_user_from_cookie(req: Request) -> Optional[UserEntity]:
    session_token = req.cookies.get('cbo_session_token')
    if not session_token:
        return None
    try:
        return sdk.sessions.validate_token(session_token)
    except Exception:
        # use more sophisticated error handling in production
        return None


def get_authenticated_user_from_authorization_header(req: Request) -> Optional[UserEntity]:
    session_token = req.headers.get('Authorization')
    if not session_token:
        return None
    session_token = session_token.removeprefix("Bearer ")
    try:
        return sdk.sessions.validate_token(session_token)
    except Exception:
        # use more sophisticated error handling in production
        return None



def get_user_identifiers(user_id: str) -> IdentifierList:
    return sdk.identifiers.list_identifiers(user_id=user_id)
