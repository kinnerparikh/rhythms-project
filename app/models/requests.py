from pydantic import BaseModel
from typing import Optional

class NewChat(BaseModel):
    user_id: str
    context: Optional[str] = None