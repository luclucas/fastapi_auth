from pydantic import BaseModel

class UserCreated(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True