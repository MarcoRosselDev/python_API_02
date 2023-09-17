from fastapi import APIRouter, status, Depends
from .. import schemas, oauth2, models
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"])

@router.post("/",
    status_code=status.HTTP_201_CREATED, 
    #response_model=schemas.Post
    )
def vote_post(
    post: schemas.VotePost,
    db: Session = Depends(get_db), 
    user_id: int=Depends(oauth2.get_current_user)
):
    #db.query(models.Vote).
    new_post = models.Vote(
        user_id=user_id.id, # --> owner_id de schema le damos el valor de la llave foranea decodificada.
        post_id=post.id # --> lo demas lo extraemos del schema post. convertido en dictionari.
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(post)
    return new_post