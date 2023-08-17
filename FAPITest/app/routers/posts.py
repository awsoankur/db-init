from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional,List
from fastapi import Depends,HTTPException, Query, Response, APIRouter
from fastapi.encoders import jsonable_encoder
from .. import schemas,models,oauth2,utils

router =APIRouter(
    prefix= "/posts"
)

@router.get("/")
def get_post(db: Session = Depends(get_db),userid:int = Depends(oauth2.get_current_user)):
    results = db.query(models.Post).all()
    return results

@router.post("/",status_code=200,response_model=schemas.PostIn )
def post(post:schemas.PostCreate, db : Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    newPost = models.Post(user_id=user_id.id, **post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost

@router.get(
        "/{id}",
        response_model=schemas.Post,
        response_model_exclude_none=True,
)
def fetch_post(id:int ,expand:List[str] = Query([]),  db: Session = Depends(get_db),userid:int = Depends(oauth2.get_current_user)):
    post =  db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).first()
    num_votes = post.votes
    if not post:
        raise HTTPException(status_code=404,detail=f"post with id = {id} not found")
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=404,detail=f"post with id = {id} not found")
    response = jsonable_encoder(post)
    response["total_votes"] = num_votes
    response = utils.expand_util(response,expand,db)
    return response

@router.delete("/{id}",status_code=204)
def delete_post(id, db : Session = Depends(get_db),userid:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise HTTPException(status_code=404 ,detail=f"post with id = {id} not found")
    
    if post.first().user_id!=userid.id:
        raise HTTPException(status_code=403,details="authorization error" )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)

@router.put("/{id}",status_code=201,response_model=schemas.PostIn)
def updatePUTpost(id: int,post:schemas.PostCreate,db: Session = Depends(get_db),userid:int = Depends(oauth2.get_current_user)):

    update_query=db.query(models.Post).filter(models.Post.id==id)
    new_post = update_query.first()
    if new_post ==None:
        raise HTTPException(status_code= 404 ,detail=f"post with id = {id} not found")
    if new_post.user_id!=userid.id:
        raise HTTPException(status_code=403,detail="authorization error" )

    update_query.update(post.dict(),synchronize_session=False)
    db.commit() 
    return update_query.first()
