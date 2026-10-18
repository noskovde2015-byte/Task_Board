from pydantic import BaseModel, ConfigDict, Field


class BoardCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    is_public: bool = Field(default=True)


class BoardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    owner_id: int
    is_public: bool
