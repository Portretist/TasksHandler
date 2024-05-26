from database import models, schemas
from database.database_conaction import session


async def add_task(task_body: schemas.CreateTaskSchema):
    new_task = models.TaskModel(**task_body.model_dump())
    session.add(new_task)


async def add_tag(tag_name: str):
    new_tag = models.TagModel(name=tag_name.lower())
    session.add(new_tag)
