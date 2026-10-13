from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserAuth(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_first_bcrypt(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes")
        return value


class UserCreate(UserAuth):
    password: str = Field(min_length=8)
    username: str = Field(min_length=3, max_length=32)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
