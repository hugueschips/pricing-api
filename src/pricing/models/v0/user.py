from pydantic import BaseModel


class FirebaseUser(BaseModel):
    """Firebase user model received at login"""

    iss: str
    aud: str
    user_id: str
    sub: str
    iat: int
    exp: int
    email: str
    email_verified: bool
    firebase: dict
    uid: str


User = FirebaseUser
