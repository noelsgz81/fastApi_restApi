from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

posts = []


#Clase Publicacion
class Publicacion(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    create_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

@app.get('/')
def read_root():
    return {"Welcome": "Welcom mi first Rest API"}

@app.get('/posts')
def get_post():
    return posts

@app.post('/posts')
def save_publicacion(post : Publicacion):
    post.id = str(uuid())
    print(f"post ID: {post.id}")
    posts.append(post.dict())
    return posts[-1]

@app.get('/posts/{post_id}')
def get_post(post_id : str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post no foundddd")

@app.delete('/posts/{post_id}')
def delete_post(post_id : str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post removido correctamente"}    
    raise HTTPException(status_code=404, detail="Post no removida")

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatePost: Publicacion):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updatePost.title
            posts[index]["author"] = updatePost.author
            posts[index]["content"] = updatePost.content
            return {"message": "Post actualizada correctamente"}    
    raise HTTPException(status_code=404, detail="Post no actualizada")
    