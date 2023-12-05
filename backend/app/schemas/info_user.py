from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class InfoBase(BaseModel):
    code: int
    first_name: str
    last_name: str
    gender: