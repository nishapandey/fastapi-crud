"""from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            dbname="testdb",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed: ", error)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    id: Optional[int] = None


@app.get("/sqlalchemy/posts")
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts")
def read_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return posts


@app.get("/posts/{id}")
def read_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    try:
        cursor.execute(
            """INSERT INTO posts (title, content, published) VALUES ( % s, % s, % s) RETURNING * """,
            (post.title, post.content, post.published)
        )
        new_post = cursor.fetchone()
        conn.commit()
        return new_post
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    conn.commit()
    return updated_post
    """
