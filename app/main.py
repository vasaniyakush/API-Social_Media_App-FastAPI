#using psycopg
import time
from turtle import pos
from typing import Optional, SupportsIndex
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        # conn = psycopg2.connect(host,databse,user,passs)
        conn = psycopg2.connect(host='localhost', database='fast',
                                user='postgres', password='1973', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Dataabse connection was successful")
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "fav food", "content": "pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")  # decorator - '@' symbolizes decorator| without this decorator, root() is a normal function and not an fastapi function
# get is an HTTP method, "/" takes us to root path of the url, eg . http://127.0.0.1:8000/
def root():
    return {"message": "Hello"}


# @app.get("/login")#if we use "/login" this function will be called if we go to http://127.0.0.1:8000/login
# def login():
#     return {"message": "login page"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content: {payload['content']}"}

# title str, content str - we want these two info from post request and nothing else


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # post_dict = post.dict();
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # cursor.execute(""" INSERT INTO posts (title, content, published ) VALUES ({post.title}, {post.content}, {post.published})""") 
                                                                            #this has risk of SQL Injection
    cursor.execute(""" INSERT INTO posts (title, content, published ) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published)) #when we pass it like this, the library takes care of SQL injection
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")  # id - path parameter
# def get_post(id): id is the parameter that we receive from the request
# print(type(id))  #parameter is get as a string.
# post = find_post(int(id)); #so we convert it to string to match our dictionary
def get_post(id: int):  # so we specify the type of path parameter to be received
    # post = find_post(id)
    # if not post:  # we have to include response:Response as a parameter if we dont use raiseException
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return{"message": f"post with id {id} was not found"}
    #     # or we can do this |-vvvv
    #     raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,
    #                         detail=f"post with id {id} was not found")
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} Not Found.")
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    # indeex = find_index_post(id)
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    # my_posts.pop(indeex)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # print(post)
    # indeex = find_index_post(id)
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[indeex] = post_dict
    
    return {"message": updated_post}
