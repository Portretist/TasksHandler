from typing import Optional
from sqlalchemy import update

from database import models, schemas
from database.database_conaction import session


async def change_status(
    task_id: Optional[int or None], task_header: Optional[str or None]
) -> None:
    if task_id:
        query = (
            update(models.TaskModel)
            .where(models.TaskModel.id == task_id)
            .values(is_completed=True)
        )
    else:
        query = (
            update(models.TaskModel)
            .where(models.TaskModel.heading == task_header)
            .values(is_completed=True)
        )
    await session.execute(query)


async def edit_task(
    new_values: schemas.EditTaskSchema,
    task_id: Optional[int or None],
    task_header: Optional[str or None],
) -> None:
    data_to_update = {}
    for key, values in new_values.model_dump().items():
        data_to_update[key] = values

    if task_id:
        query = (
            update(models.TaskModel)
            .where(models.TaskModel.id == task_id)
            .values(data_to_update)
        )

    else:
        query = (
            update(models.TaskModel)
            .where(models.TaskModel.heading == task_header)
            .values(data_to_update)
        )

    await session.execute(query)
