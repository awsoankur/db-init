from fastapi import HTTPException, Depends, APIRouter
from .. import schemas,utils,models,oauth2
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/votes"
)

@router.post("/",status_code=200)
def submitvote(vote : schemas.VoteIn, db : Session =Depends(get_db),user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    
    vote_q = db.query(models.Votes).filter(models.Votes.user_id==user.id,models.Votes.post_id==vote.post_id)
    vote_db = vote_q.first()
    if vote.direction:
        if vote_db:
            raise HTTPException(status_code=409,detail=f"user {user.id} already voted for {vote.post_id}")
        new_vote = models.Votes(post_id=vote.post_id,user_id=user.id,direction=vote.direction)
        db.add(new_vote)
        db.commit()
        return {"msg": "successfully voted"}
    else:
        if not vote_db:
            raise HTTPException(status_code=404,detail=f"Vote does not exist")
        vote_q.delete(synchronize_session=False)
        db.commit()
        return { "msg": "successfully deleted"}