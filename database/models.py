import datetime
from typing import List

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped

from .database_conaction import Base


class TaskModel(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    heading = Column(String(80), nullable=False, unique=True)
    description = Column(String, nullable=False)
    deadline = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now())

    tags: Mapped[List["TagModel"]] = relationship(
        back_populates="tasks",
        secondary="task_tag_relationship",
        cascade="all, delete",
    )


class TagModel(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True, nullable=False)

    tasks: Mapped[List["TaskModel"]] = relationship(
        back_populates="tags",
        secondary="task_tag_relationship",
    )


class TaskTagRelationship(Base):
    __tablename__ = "task_tag_relationship"

    task_id = Column(ForeignKey("task.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True)
