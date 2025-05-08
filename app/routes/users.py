from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, auth, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/signup', response_model=schemas.UserOut)
def signup(user: schemas.UserCreated, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(username=user.username).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    hashed = auth.hash_password(user.password)

    new_user = models.User(username = user.username, hashed_password=hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login')
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(username=user.username).first()

    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail='Credenciais Inválidas')
    token = auth.create_access_token(data={'sub': db_user.username})
    return {"access_token": token, "token_type": "bearer"}
