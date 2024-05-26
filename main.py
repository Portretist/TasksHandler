import asyncio
from typing import Tuple, Optional

from fastapi import FastAPI

from database.database_conaction import engine, session
from database import models, schemas
from database.CRUD import CRUDInterface

app = FastAPI()
crud = CRUDInterface()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/task/all/")
async def get_all_tasks(filter_name: Optional[str] = "id"):
    return await crud.get_all_tasks(filter_name)


@app.get("/task/tag/all/")
async def get_all_tags():
    return await crud.get_all_tags()


@app.post("/task/tag/create/")
async def create_tag(tag_name: str):
    return await crud.create_tag(tag_name)


@app.post("/task/create/")
async def create_new_task(task_body: schemas.CreateTaskSchema) -> Tuple[str, int]:
    return await crud.create_task(task_body)


@app.post("/task/edit/")
async def edit_task(
    new_values: schemas.EditTaskSchema,
    task_id: Optional[int] = None,
    task_header: Optional[str] = None,
) -> Tuple[str, int]:
    return await crud.edit_task(new_values, task_id, task_header)


@app.post("/task/change_status/")
async def change_task_status(
    task_id: Optional[int] = None, task_header: Optional[str] = None
) -> Tuple[str, int]:
    return await crud.change_status(task_id, task_header)


@app.delete("/task/delete/")
async def delete_task(
    task_id: Optional[int] = None, task_header: Optional[str] = None
) -> Tuple[str, int]:
    return await crud.delete_task(task_id, task_header)
