from fastapi import Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import modelos, esquemas
from bancodedados import engine, get_db

modelos.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def inicio():
  return {'mensagem': 'Alô Mundo'}

@app.get('/posts', response_model=List[esquemas.ResponsePost])
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(modelos.Post).all()

  return posts

@app.get('/posts/{id}', response_model=esquemas.ResponsePost)
def get_post(id: int, db: Session = Depends(get_db)):
  post = db.query(modelos.Post).filter(modelos.Post.id == id).first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'Post com o id: {id} não foi encontrado')

  return post

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=esquemas.ResponsePost)
def create_post(post: esquemas.CreatePost, db: Session = Depends(get_db)):
  novoPost = modelos.Post(**post.dict())
  db.add(novoPost)
  db.commit()
  db.refresh(novoPost)

  return novoPost

@app.put('/posts/{id}')
def update_post(id: int, post: esquemas.CreatePost, db: Session = Depends(get_db), response_model=esquemas.ResponsePost):
  atualizado = db.query(modelos.Post).filter(modelos.Post.id == id)

  if atualizado.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post com o id: {id} não foi encontrado')

  atualizado.update(post.dict(), synchronize_session=False)
  db.commit()

  return atualizado.first()

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  removido = db.query(modelos.Post).filter(modelos.Post.id == id)

  if removido.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post com o id: {id} não foi encontrado')

  removido.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

