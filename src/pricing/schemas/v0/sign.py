from pydantic import BaseModel


class SignupSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "007@mi6.uk", "password": "better than Ethan Hunt"}
        }


class SigninSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "007@mi6.uk", "password": "better than Ethan Hunt"}
        }
