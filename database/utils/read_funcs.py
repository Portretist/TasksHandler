from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.database_conaction import session
from database import models


async def get_all_tasks(filter_name: str = "id") -> List:
    if filter_name == "id":
        query = (
            select(models.TaskModel)
            .options(selectinload(models.TaskModel.tags))
            .order_by(models.TaskModel.id)
        )
    elif filter_name == "heading":
        query = (
            select(models.TaskModel)
            .options(selectinload(models.TaskModel.tags))
            .order_by(models.TaskModel.heading)
        )
    elif filter_name == "created_at":
        query = (
            select(models.TaskModel)
            .options(selectinload(models.TaskModel.tags))
            .order_by(models.TaskModel.created_at)
        )
    elif filter_name == "deadline":
        query = (
            select(models.TaskModel)
            .options(selectinload(models.TaskModel.tags))
            .order_by(models.TaskModel.deadline)
        )
    elif filter_name == "is_completed":
        query = (
            select(models.TaskModel)
            .options(selectinload(models.TaskModel.tags))
            .order_by(models.TaskModel.is_completed)
        )
    else:
        query = select(models.TaskModel).options(selectinload(models.TaskModel.tags))

    result = await session.execute(query)
    result = result.scalars().all()

    if filter_name == "tags":
        return sorted(result, key=lambda task: task.tags)
    return result


async def get_all_tags() -> List:
    query = select(models.TagModel)
    get_tag = await session.execute(query)
    return get_tag.scalars().all()


async def get_tag_by_name(tag_name: str) -> str:
    query = select(models.TagModel).where(models.TagModel.name == tag_name.lower())
    get_tag = await session.execute(query)
    result = get_tag.scalars().all()
    if result:
        return result[0]
    else:
        return tag_name
