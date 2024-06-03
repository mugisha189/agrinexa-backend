from pydantic import BaseModel
from typing import Optional, List


class CommunityQuestion(BaseModel):
    title: str
    description: str
    user_id: str
    upVotes: int = 0
    downVotes: int = 0
    solutions: List[str] = []
    
class CreateCommunityQuestion(BaseModel):
    title: str
    description: str


class CommunitySolution(BaseModel):
    id: Optional[str]
    question_id: str
    body: str
    user_id: str
    upVotes: int = 0
    downVotes: int = 0
