import base64

import requests
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from firebase_admin import auth, credentials, initialize_app
from loguru import logger

from pricing.core.settings import settings
from pricing.models.v0.user import User
from pricing.schemas.v0.sign import SignupSchema

DECODED_FIREBASE_PRIVATE_KEY = (
    base64.b64decode(settings.FIREBASE_PRIVATE_KEY).decode("ascii").replace("\\n", "\n")
)


# Initialize Firebase Admin SDK with your service account credentials
firebase_credentials = {
    "type": "service_account",
    "project_id": settings.FIREBASE_PROJECT_ID,
    "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
    "private_key": DECODED_FIREBASE_PRIVATE_KEY,
    "client_email": settings.FIREBASE_CLIENT_EMAIL,
    "client_id": settings.FIREBASE_CLIENT_ID,
    "auth_uri": settings.FIREBASE_AUTH_URI,
    "token_uri": settings.FIREBASE_TOKEN_URI,
    "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": settings.FIREBASE_CLIENT_X509_CERT_URL,
    "universe_domain": "googleapis.com",
}
cred = credentials.Certificate(firebase_credentials)


# Initialize Direbase admin app
initialize_app(cred)


router = APIRouter(
    prefix="/v0/firebase",
    tags=["v0"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/signup/",
    include_in_schema=False,
)
@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
)
async def create_an_account(body: SignupSchema):
    # Use Firebase Admin SDK to create a new user
    try:
        user = auth.create_user(email=body.email, password=body.password)
        logger.success(f"Account {user.email} just got created.")
        return JSONResponse(
            content={"message": f"Account succesfully created for user {user.uid}"},
            status_code=201,
        )
    except auth.EmailAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/signin/",
    include_in_schema=False,
)
@router.post("/signin")
async def create_access_token(body: SignupSchema):
    rest_api_url = (
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    )
    request_body = body.dict()
    request_body["returnSecureToken"] = True
    response = requests.post(
        rest_api_url,
        params={"key": settings.FIREBASE_WEB_API_KEY},
        data=request_body,
    )
    if response.status_code == 200:
        logger.success(f"Account {body.email} just logged in.")
        return response.json()
    else:
        return Response(
            status_code=response.status_code,
            content=response.json().get("error", {}).get("message", {}),
        )


@router.get(
    "/ping/",
    include_in_schema=False,
)
@router.get(
    "/ping",
    status_code=status.HTTP_200_OK,
    response_model=User | None,
    responses={401: {}},
)
async def validate_token(request: Request):
    headers = request.headers
    jwt = headers.get("Authorization").replace("Bearer ", "")
    try:
        token = auth.verify_id_token(id_token=jwt)
        user = User(**token)
        logger.success(f"Account {user.email} just pinged.")
        return user
    except Exception as e:
        msg = f"Invalid token: {e}"
        logger.error(msg)
        raise HTTPException(status_code=401, detail=msg)


@router.get(
    "/pong",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def authenticate_user(user: User = Depends(validate_token)):
    return user
