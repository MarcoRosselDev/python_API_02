from fastapi import APIRouter, status, Depends, HTTPException
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
    vote: schemas.VotePost,
    db: Session = Depends(get_db), 
    user_id: int=Depends(oauth2.get_current_user)
):
    # primero filtramos el post
    #vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.id, models.Vote.user_id == user_id.id)
    foudn_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.id, models.Vote.user_id == user_id.id)
    primero = foudn_vote.first()

    if primero:
        #delete
        foudn_vote.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="le quitamos el voto, por que ya tenia")
        # ojo con raise, deve ir al ultimo, lo que sigue no se ejecuta
    else:
        new_post = models.Vote(
        user_id=user_id.id, # --> owner_id de schema le damos el valor de la llave foranea decodificada.
        post_id=vote.id # --> lo demas lo extraemos del schema post. convertido en dictionari.
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

    return new_post