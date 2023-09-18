from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, db

router = APIRouter()

@router.post("/todos/")
def create_todo(todo: models.TodoCreate, db: Session = Depends(db.get_database)):
    # Implementation of creating a to-do item
    db_todo = models.Todo(**todo.dict(), owner_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/todos/")
def get_todos(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_database)):
    # Implementation of listing to-do items
    todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).offset(skip).limit(limit).all()
    return todos

@router.get("/todos/{todo_id}/")
def get_todo(todo_id: int, db: Session = Depends(db.get_database)):
    # Implementation of getting a specific to-do item
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/todos/{todo_id}/")
def update_todo(todo_id: int, todo: models.TodoUpdate, db: Session = Depends(db.get_database)):
    # Implementation of updating a to-do item
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.title:
        db_todo.title = todo.title
    if todo.description:
        db_todo.description = todo.description
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todos/{todo_id}/")
def delete_todo(todo_id: int, db: Session = Depends(db.get_database)):
    # Implementation of deleting a to-do item
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
