from pydantic import BaseModel

class Document(BaseModel):
    id: str
    path: str
    content: str
    readed: bool