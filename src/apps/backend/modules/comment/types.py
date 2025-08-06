from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Comment:
    id: str
    task_id: str
    content: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class GetCommentParams:
    comment_id: str


@dataclass(frozen=True)
class GetCommentsParams:
    task_id: str


@dataclass(frozen=True)
class CreateCommentParams:
    task_id: str
    content: str


@dataclass(frozen=True)
class UpdateCommentParams:
    comment_id: str
    content: str


@dataclass(frozen=True)
class DeleteCommentParams:
    comment_id: str


@dataclass(frozen=True)
class CommentDeletionResult:
    comment_id: str
    deleted_at: datetime
    success: bool


@dataclass(frozen=True)
class CommentErrorCode:
    NOT_FOUND: str = "COMMENT_ERR_01"
    BAD_REQUEST: str = "COMMENT_ERR_02"
    TASK_NOT_FOUND: str = "COMMENT_ERR_03" 