import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from pricing.api.v0.firebase import User, validate_token
from pricing.core.settings import BASIC_AUTHS

router = APIRouter(
    prefix="/v0",
    tags=["v0"],
    responses={404: {"description": "Not found"}},
    include_in_schema=True,
)


@router.post(
    "/quote/",
    include_in_schema=False,
)
@router.post(
    "/quote",
    status_code=status.HTTP_200_OK,
)
async def post_quote(
    body: dict = {},
    user: User = Depends(validate_token),
):
    """Post anything as a dictionary and store it into the selected Mongo database"""
    if body == {}:
        return Response(
            content="Empty body. Simply ignored.",
            status_code=403,
        )

    return True


@router.get(
    "/price/",
    include_in_schema=False,
)
@router.get(
    "/price",
    status_code=status.HTTP_200_OK,
)
async def get_trip(
    id: str,
    # user: User = Depends(validate_token),
):
    """Get price based on quote ID"""
    return 1000


security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")

    # Check if the provided credentials match any pair from the list
    for username, password in BASIC_AUTHS:
        correct_username_bytes = username.encode("utf8")
        correct_password_bytes = password.encode("utf8")

        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )

        if is_correct_username and is_correct_password:
            return credentials.username

    # If no match is found, raise HTTPException
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@router.post(
    "/basic_auth/",
    include_in_schema=False,
)
@router.post(
    "/basic_auth",
    status_code=status.HTTP_200_OK,
)
async def upload_locations_batch(
    username: Annotated[str, Depends(get_current_username)],
    body: list = [],
):
    return Response(
        content="Hello",
        status_code=200,
    )
