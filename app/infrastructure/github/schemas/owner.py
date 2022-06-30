from pydantic import BaseModel


class Owner(BaseModel):
    id: int
    login: str
    html_url: str
    avatar_url: str
