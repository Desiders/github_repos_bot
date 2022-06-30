from typing import Optional

from pydantic import BaseModel


class Licence(BaseModel):
    name: str
    url: Optional[str]
