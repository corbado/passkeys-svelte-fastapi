from app.routes import router as api_router
from app.utils.authentication import get_authenticated_user_from_cookie, \
    get_authenticated_user_from_authorization_header

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def attach_user(request: Request, call_next):
    corbado_user = (get_authenticated_user_from_cookie(request) or
                    get_authenticated_user_from_authorization_header(request))
    request.state.corbado_user = corbado_user
    response = await call_next(request)
    return response



app.include_router(api_router, prefix="/api")
