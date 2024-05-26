import asyncio
from typing import Tuple, List, Callable, Optional
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import ResponseValidationError


from database import schemas, models
from database.database_conaction import session
from database.utils import create_funcs, read_funcs, update_funcs, deleat_funcs


def error_handler(func: Callable):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            await session.commit()
            return result
        except IntegrityError:
            await session.rollback()
            return "This tag already exist", 400
        except ResponseValidationError:
            return "Input wrong data", 400
        except Exception as e:
            await session.rollback()
            return {"error_name": e.__class__.__name__, "error_text": str(e)}, 500

    return wrapper


class CRUDInterface:
    @error_handler
    async def create_task(self, task_body: schemas.CreateTaskSchema) -> Tuple[str, int]:
        if task_body.tags:
            tags = await self.check_tag(task_body.tags)
            task_body.tags = tags

        func = asyncio.create_task(create_funcs.add_task(task_body))
        await func
        return "Task created", 201

    @error_handler
    async def create_tag(self, tag_name) -> Tuple[str, int]:
        await create_funcs.add_tag(tag_name)
        return "Tag created", 201

    @error_handler
    async def check_tag(self, tags: List) -> List[schemas.GetTagSchema]:
        result = [await read_funcs.get_tag_by_name(tag_name) for tag_name in tags]

        received_tags = list(
            filter(lambda tag: isinstance(tag, models.TagModel), result)
        )
        tags_to_create = list(filter(lambda tag: isinstance(tag, str), result))

        [await self.create_tag(tag_name) for tag_name in tags_to_create]
        new_tags = [
            await read_funcs.get_tag_by_name(tag_name) for tag_name in tags_to_create
        ]
        received_tags.extend(new_tags)

        return received_tags

    @error_handler
    async def get_all_tasks(self, filter_name: str) -> Tuple[List, int]:
        return await read_funcs.get_all_tasks(filter_name), 200

    @error_handler
    async def get_all_tags(self) -> Tuple[List, int]:
        return await read_funcs.get_all_tags(), 200

    @error_handler
    async def delete_task(
        self, task_id: Optional[int or None], task_header: Optional[str or None]
    ) -> Tuple[str, int]:
        await deleat_funcs.delete_task(task_id, task_header)
        return "Task deleted", 200

    @error_handler
    async def change_status(
        self, task_id: Optional[int or None], task_header: Optional[str or None]
    ) -> Tuple[str, int]:
        await update_funcs.change_status(task_id, task_header)
        return "Task completed", 200

    @error_handler
    async def edit_task(
        self,
        new_values: schemas.EditTaskSchema,
        task_id: Optional[int or None],
        task_header: Optional[str or None],
    ) -> Tuple[str, int]:
        if new_values.tags:
            new_values.tags = await self.check_tag(new_values.tags)
        await update_funcs.edit_task(new_values, task_id, task_header)
        return "Task edited", 200


if __name__ == "__main__":
    crud = CRUDInterface()
