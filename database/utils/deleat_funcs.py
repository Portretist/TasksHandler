from typing import Optional
from sqlalchemy import delete

from database import models
from database.database_conaction import session


async def delete_task(
    task_id: Optional[int or None], task_header: Optional[str or None]
) -> None:
    if task_id:
        query = delete(models.TaskModel).where(models.TaskModel.id == task_id)
    else:
        query = delete(models.TaskModel).where(models.TaskModel.heading == task_header)
    await session.execute(query)
