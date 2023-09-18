from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, db

router = APIRouter()

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register/")
def register_user(user: models.UserCreate, db: Session = Depends(db.get_database)):
    # Implementation of user registration
    db_user = models.User(username=user.username, email=user.email, hashed_password=pwd_context.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@router.post("/login/")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_database)):
    # Implementation of user login
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # Generate JWT token and return it
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
