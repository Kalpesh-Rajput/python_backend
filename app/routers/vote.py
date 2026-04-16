from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from .. import schemas,database,model,oauth2 

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.vote,db:Session = Depends(database.get_db),
         current_user : int = Depends(oauth2.get_current_user)):
    
    pass

