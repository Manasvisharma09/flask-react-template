from modules.application.errors import AppError
from modules.comment.types import CommentErrorCode


class CommentBadRequestError(AppError):
    def __init__(self, message: str):
        super().__init__(message=message, code=CommentErrorCode.BAD_REQUEST, http_code=400)


class CommentNotFoundError(AppError):
    def __init__(self, message: str):
        super().__init__(message=message, code=CommentErrorCode.NOT_FOUND, http_code=404)


class TaskNotFoundError(AppError):
    def __init__(self, message: str):
        super().__init__(message=message, code=CommentErrorCode.TASK_NOT_FOUND, http_code=404) 