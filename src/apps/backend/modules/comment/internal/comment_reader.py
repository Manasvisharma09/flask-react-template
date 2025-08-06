from datetime import datetime
from typing import Optional

from modules.comment.errors import CommentNotFoundError
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import Comment, GetCommentParams, GetCommentsParams
from modules.task.internal.store.task_repository import TaskRepository
from modules.task.errors import TaskNotFoundError


class CommentReader:
    @staticmethod
    def get_comment(*, params: GetCommentParams) -> Comment:
        comment_model = CommentRepository.get_comment_by_id(comment_id=params.comment_id)

        if comment_model is None:
            raise CommentNotFoundError(f"Comment with id {params.comment_id} not found")

        return Comment(
            id=str(comment_model.id),
            task_id=comment_model.task_id,
            content=comment_model.content,
            created_at=comment_model.created_at,
            updated_at=comment_model.updated_at,
        )

    @staticmethod
    def get_comments(*, params: GetCommentsParams) -> list[Comment]:
        # First verify that the task exists
        task_model = TaskRepository.get_task_by_id(task_id=params.task_id)
        if task_model is None:
            raise TaskNotFoundError(f"Task with id {params.task_id} not found")

        comment_models = CommentRepository.get_comments_by_task_id(task_id=params.task_id)

        return [
            Comment(
                id=str(comment_model.id),
                task_id=comment_model.task_id,
                content=comment_model.content,
                created_at=comment_model.created_at,
                updated_at=comment_model.updated_at,
            )
            for comment_model in comment_models
        ] 