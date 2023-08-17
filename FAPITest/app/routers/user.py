from json import JSONEncoder
from fastapi import HTTPException, Depends, APIRouter, Query
from .. import schemas,utils,models
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException



router = APIRouter(
    prefix="/users"
)

@router.post("/",response_model=schemas.UserOut)
def create_user(user: schemas.UserIn,db : Session = Depends(get_db)):
    hashpwd = utils.hash(user.password)
    user.password=hashpwd
    newAccount = models.Account()
    db.add(newAccount)
    db.commit()
    newUser = models.User(**user.dict(),account_id= newAccount.id)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser

@router.get(
        "/{id}",
        response_model=schemas.User,
        response_model_exclude_none= True,       
)
def get_user(id:int,expand : List[str] = Query([]) , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    
    if user == None:
        raise HTTPException(status_code=404, detail=f"User with id = {id} not found")
    response = jsonable_encoder(user)
    response = utils.expand_util(response,expand,db)
    return response