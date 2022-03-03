from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from bancodedados import Base

class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True, nullable=False)
  titulo = Column(String, nullable=False)
  conteudo = Column(String, nullable=False)
  publicado = Column(Boolean, server_default='TRUE', nullable=False)
  criado_em = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))