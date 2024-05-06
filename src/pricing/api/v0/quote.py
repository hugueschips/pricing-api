from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from pricing.api.v0.basic_auth import get_current_username

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
    username: Annotated[str, Depends(get_current_username)],
    body: dict = {},
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
    username: Annotated[str, Depends(get_current_username)],
    id: str | None = None,
):
    """Get price based on quote ID"""
    return 1000
