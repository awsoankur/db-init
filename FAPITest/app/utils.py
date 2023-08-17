from passlib.context import CryptContext
from . import models
from fastapi.encoders import jsonable_encoder

pwd_context = CryptContext(schemes=["bcrypt"])

def hash(s):
    return pwd_context.hash(s)

def verify(user,testUser):
    return pwd_context.verify(testUser.password,user.password)

def expand_util(response,expand,db):
    for query in expand:
        current = response
        path = query.split(".")
        for node in path:
            if node == "account":
                account_id = current["account_id"]
                del current["account_id"]
                account = db.query(models.Account).filter(models.Account.id==account_id).first()
                current["account"]=jsonable_encoder(account)
                current=current["account"]
            if node == "user":
                user_id = current["user_id"]
                del current["user_id"]
                user = db.query(models.User).filter(models.User.id==user_id).first()
                current["user"]=jsonable_encoder(user)
                current=current["user"]
            if node == "votes":
                current["votes"] = jsonable_encoder(
                    db.query(models.Votes).filter(
                        models.Votes.post_id == models.Post.id
                    ).all()
                )
                current = current["votes"]
    return response