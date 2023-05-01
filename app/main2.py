from fastapi import FastAPI
# from . import models, schemas,utils
from .database import engine, get_db
from .routers import post,user,auth,votes
from fastapi.middleware.cors import CORSMiddleware
# from .schemas import Post




#-----------------------------------DATABASE CREATION----------------------------
# models.Base.metadata.create_all(bind=engine) #we dont need this because now we use alembic 
                                                #for table creation

app = FastAPI()
origins = ["*"]  # currently allows all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)
#---------------------------------------********-------------------------------------


# while True:
#     try:
#         # conn = psycopg2.connect(host,databse,user,passs)
#         conn = psycopg2.connect(host='localhost', database='fast',
#                                 user='postgres', password='1973', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Dataabse connection was successful")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)


@app.get("/") 
def root():
    # f = open("D:\\Python_projects\\Fast\\attendance\\test.html",'r')
    return {"message": "You called a ginnie, i'll grant you 3 wishes!!!"}

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):

#     posts = db.query(models.Post)
#     print(posts)
#     return {"data" : "ok"}


#-----------------------------POSTS--------------------------------------------------
# #------------------------------GET----------------------------------------------------

# @app.get("/posts",response_model= List[schemas.PostResponse])
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts


# @app.get("/posts/{id}",response_model= schemas.PostResponse)
# def get_post(id: int,db:Session = Depends(get_db)):  # so we specify the type of path parameter to be received
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     print(post)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} Not Found.")
#     return post

# #---------------------------POST----------------------------------------------------------

# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
# def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db)):
#     # new_post = models.Post(title=post.title, content=post.content, published=post.published)
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post

# #---------------------------DELETE--------------------------------------------------------

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int,db:Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id)
#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with {id} does not exist")
#     post.delete(synchronize_session=False) 
#     db.commit()
#     # my_posts.pop(indeex)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# #-----------------------------PUT/UPDATE------------------------------------------------------

# @app.put("/posts/{id}",response_model= schemas.PostResponse)
# def update_post(id: int, post:schemas.PostCreate, db:Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     if post_query.first() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with {id} does not exist")
#     post_query.update(post.dict(),synchronize_session=False)
#     db.commit()

#     # post_dict = post.dict() 
#     # post_dict["id"] = id
#     # my_posts[indeex] = post_dict
    
#     return  post_query.first()
#------------------------------*********-----------------------------------------


#---------------------------------USERS---------------------------------------------


# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse)
# def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):

#     #hash the pasword - user.password
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get("/users/{id}",response_model=schemas.UserResponse)
# def get_user(id:int, db:Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                              detail=f"User with id {id} does not exist")

#     return user
