from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.db import db

from app.auth import get_current_active_user
from app.models.auth import UserModel

from app.schemas.todo import TodoSchema
from app.schemas.todo import TodosSchema
from app.models.todo import TodoModel


router = APIRouter()


@router.get("/todo/", response_model=TodosSchema)
async def get_todos(user: UserModel = Depends(get_current_active_user)):
    todos = await TodoModel.query.where(
        db.and_(
            TodoModel.user_id == user.id,
        )
    ).order_by(TodoModel.id.desc()).limit(200).gino.all()

    return TodosSchema.parse_obj({'objects': [x.to_dict() for x in todos]})


@router.post("/todos/", response_model=TodoSchema, status_code=201)
async def add_todo(
        todo_schema: TodoSchema,
        user: UserModel = Depends(get_current_active_user)
):
    todo = await TodoModel.create(
        text=todo_schema.text,
        completed=todo_schema.completed,
        user_id=user.id
    )
    return TodoSchema.parse_obj(todo.to_dict())


@router.get("/todos/{todo_id}/", response_model=TodoSchema)
async def get_todo(todo_id: int, user: UserModel = Depends(get_current_active_user)):
    todo = await TodoModel.query.where(
        db.and_(
            TodoModel.user_id == user.id,
            TodoModel.id == todo_id,
        )
    ).gino.first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todos are not found")

    return TodoSchema.parse_obj(todo.to_dict())


@router.put("/todos/{todo_id}/", response_model=TodoSchema)
async def edit_todo(
        todo_id: int,
        todo_schema: TodoSchema,
        user: UserModel = Depends(get_current_active_user)
):
    todo = await TodoModel.query.where(
        db.and_(
            TodoModel.user_id == user.id,
            TodoModel.id == todo_id,
        )
    ).gino.first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todos are not found")

    await todo.update(
        text=todo_schema.text,
        completed=todo_schema.completed,
    ).apply()

    return TodoSchema.parse_obj(todo.to_dict())


@router.delete("/todos/{todo_id}/", status_code=204)
async def delete_todo(
        todo_id: int,
        user: UserModel = Depends(get_current_active_user)
):
    todo = await TodoModel.query.where(
        db.and_(
            TodoModel.user_id == user.id,
            TodoModel.id == todo_id,
        )
    ).gino.first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todos are not found")

    await todo.delete()

    return {}
