from dataclasses import asdict
from typing import Optional

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.comment.errors import CommentBadRequestError
from modules.comment.comment_service import CommentService
from modules.comment.types import (
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentsParams,
    GetCommentParams,
    UpdateCommentParams,
)


class CommentView(MethodView):
    @access_auth_middleware
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()

        if request_data is None:
            raise CommentBadRequestError("Request body is required")

        if not request_data.get("task_id"):
            raise CommentBadRequestError("Task ID is required")

        if not request_data.get("content"):
            raise CommentBadRequestError("Content is required")

        create_comment_params = CreateCommentParams(
            task_id=request_data["task_id"], content=request_data["content"]
        )

        created_comment = CommentService.create_comment(params=create_comment_params)
        comment_dict = asdict(created_comment)

        return jsonify(comment_dict), 201

    @access_auth_middleware
    def get(self, comment_id: Optional[str] = None) -> ResponseReturnValue:
        if comment_id:
            # Get a specific comment
            comment_params = GetCommentParams(comment_id=comment_id)
            comment = CommentService.get_comment(params=comment_params)
            comment_dict = asdict(comment)
            return jsonify(comment_dict), 200
        else:
            # Get comments for a task
            task_id = request.args.get("task_id")
            if not task_id:
                raise CommentBadRequestError("Task ID is required as query parameter")

            comments_params = GetCommentsParams(task_id=task_id)
            comments = CommentService.get_comments(params=comments_params)
            comments_dict = [asdict(comment) for comment in comments]

            return jsonify(comments_dict), 200

    @access_auth_middleware
    def put(self, comment_id: str) -> ResponseReturnValue:
        request_data = request.get_json()

        if request_data is None:
            raise CommentBadRequestError("Request body is required")

        if not request_data.get("content"):
            raise CommentBadRequestError("Content is required")

        update_comment_params = UpdateCommentParams(
            comment_id=comment_id, content=request_data["content"]
        )

        updated_comment = CommentService.update_comment(params=update_comment_params)
        comment_dict = asdict(updated_comment)

        return jsonify(comment_dict), 200

    @access_auth_middleware
    def delete(self, comment_id: str) -> ResponseReturnValue:
        delete_params = DeleteCommentParams(comment_id=comment_id)
        deletion_result = CommentService.delete_comment(params=delete_params)
        result_dict = asdict(deletion_result)

        return jsonify(result_dict), 200 