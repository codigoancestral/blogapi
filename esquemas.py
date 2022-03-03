from pydantic import BaseModel
from datetime import datetime

class BasePost(BaseModel):
  titulo: str
  conteudo: str
  publicado: bool = True

class CreatePost(BasePost):
  pass

class ResponsePost(BasePost):
  id: int
  criado_em: datetime

  class Config:
    orm_mode = True