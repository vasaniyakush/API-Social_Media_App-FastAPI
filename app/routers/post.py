from statistics import mode
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Dict, Optional, SupportsIndex, List, Tuple
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
#-----------------------------POSTS--------------------------------------------------
#------------------------------GET----------------------------------------------------

@router.get("/",response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    print("here")
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts

@router.get("/all", response_model=List[schemas.PostOut])
# @router.get("/all",response_model= dict{"len":int,"data":List[schemas.PostResponse]} )
def get_all_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
limit: int = 10,skip: int = 0): # here limit and skip is api parameter
    # print(limit)
    
    posts = db.query(models.Post).limit(limit).offset(skip).all() # limit the number of results #off set, number of results skipped from beginning
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # results = db.query(models.Post)
    # print(results)
    # print(len(posts))
    return results;
    # return {"len": len(posts),"data": posts}


@router.get("/{id}",response_model= schemas.PostResponse)
def get_post(id: int,db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):  # so we specify the type of path parameter to be received
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(*post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} Not Found.")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No authorized to perform requested action")
    return post

#---------------------------POST----------------------------------------------------------

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user.id)
    # up_post = post.dict();
    # up_post.update({"owner_id":current_user.id})
    # new_post = models.Post(**up_post)
    new_post = models.Post( **post.dict(),owner_id=current_user.id)    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#---------------------------DELETE--------------------------------------------------------

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested operation")

    post_query.delete(synchronize_session=False) 
    db.commit()
    # my_posts.pop(indeex)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#-----------------------------PUT/UPDATE------------------------------------------------------

@router.put("/{id}",response_model= schemas.PostResponse)
def update_post(id: int, updated_post:schemas.PostCreate, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested operation")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    # post_dict = post.dict() 
    # post_dict["id"] = id
    # my_posts[indeex] = post_dict
    
    return  post_query.first() 