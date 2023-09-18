from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, db

router = APIRouter()

@router.get("/profile/")
def get_user_profile(user_id: int, db: Session = Depends(db.get_database)):
    # Implementation of getting user profile
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/profile/")
def update_user_profile(user_id: int, user: models.UserUpdate, db: Session = Depends(db.get_database)):
    # Implementation of updating user profile
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user
