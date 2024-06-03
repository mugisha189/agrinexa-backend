from pydantic import BaseModel
from app.api.users.models import User
from app.api.fields.models import Field
from typing import List

class DashboardModel(BaseModel):
    user: User
    fields: List[Field]
    tips: List[dict]
