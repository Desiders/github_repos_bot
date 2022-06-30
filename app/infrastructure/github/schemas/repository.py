from typing import Optional

from pydantic import BaseModel

from .licence import Licence
from .owner import Owner


class Repository(BaseModel):
    id: int
    name: str
    full_name: str
    html_url: str
    description: Optional[str]
    stargazers_count: int
    language: Optional[str]
    forks_count: int
    owner: Owner
    license: Optional[Licence]
