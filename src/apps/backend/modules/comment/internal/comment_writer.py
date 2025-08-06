from datetime import datetime

from modules.comment.errors import CommentNotFoundError, TaskNotFoundError
from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import (
    Comment,
    CommentDeletionResult,
    CreateCommentParams,
    DeleteCommentParams,
    UpdateCommentParams,
)
from modules.task.internal.store.task_repository import TaskRepository


class CommentWriter:
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        # First verify that the task exists
        task_model = TaskRepository.get_task_by_id(task_id=params.task_id)
        if task_model is None:
            raise TaskNotFoundError(f"Task with id {params.task_id} not found")

        comment_model = CommentModel(
            task_id=params.task_id,
            content=params.content,
        )

        created_comment_model = CommentRepository.create_comment(comment_model=comment_model)

        return Comment(
            id=str(created_comment_model.id),
            task_id=created_comment_model.task_id,
            content=created_comment_model.content,
            created_at=created_comment_model.created_at,
            updated_at=created_comment_model.updated_at,
        )

    @staticmethod
    def update_comment(*, params: UpdateCommentParams) -> Comment:
        # First verify that the comment exists
        existing_comment_model = CommentRepository.get_comment_by_id(comment_id=params.comment_id)
        if existing_comment_model is None:
            raise CommentNotFoundError(f"Comment with id {params.comment_id} not found")

        comment_model = CommentModel(
            task_id=existing_comment_model.task_id,
            content=params.content,
            created_at=existing_comment_model.created_at,
            updated_at=datetime.now(),
        )

        updated_comment_model = CommentRepository.update_comment(
            comment_id=params.comment_id, comment_model=comment_model
        )

        if updated_comment_model is None:
            raise CommentNotFoundError(f"Comment with id {params.comment_id} not found")

        return Comment(
            id=str(updated_comment_model.id),
            task_id=updated_comment_model.task_id,
            content=updated_comment_model.content,
            created_at=updated_comment_model.created_at,
            updated_at=updated_comment_model.updated_at,
        )

    @staticmethod
    def delete_comment(*, params: DeleteCommentParams) -> CommentDeletionResult:
        # First verify that the comment exists
        existing_comment_model = CommentRepository.get_comment_by_id(comment_id=params.comment_id)
        if existing_comment_model is None:
            raise CommentNotFoundError(f"Comment with id {params.comment_id} not found")

        success = CommentRepository.delete_comment(comment_id=params.comment_id)

        return CommentDeletionResult(
            comment_id=params.comment_id,
            deleted_at=datetime.now(),
            success=success,
        ) 