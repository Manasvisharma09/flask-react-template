import pytest
from server import app
from modules.comment.types import CommentErrorCode
from tests.modules.task.base_test_task import BaseTestTask

class TestCommentApi(BaseTestTask):
    def create_task_and_get_id(self, account, token):
        task_data = {"title": self.DEFAULT_TASK_TITLE, "description": self.DEFAULT_TASK_DESCRIPTION}
        response = self.make_authenticated_request("POST", account.id, token, data=task_data)
        assert response.status_code == 201
        return response.json["id"]

    def test_create_comment_success(self):
        account, token = self.create_account_and_get_token()
        task_id = self.create_task_and_get_id(account, token)
        comment_data = {"task_id": task_id, "content": "Test comment"}
        with app.test_client() as client:
            response = client.post(
                "/api/comments",
                json=comment_data,
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 201
            assert response.json["task_id"] == task_id
            assert response.json["content"] == "Test comment"

    def test_create_comment_missing_content(self):
        account, token = self.create_account_and_get_token()
        task_id = self.create_task_and_get_id(account, token)
        comment_data = {"task_id": task_id}
        with app.test_client() as client:
            response = client.post(
                "/api/comments",
                json=comment_data,
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 400
            assert response.json["code"] == CommentErrorCode.BAD_REQUEST

    def test_create_comment_invalid_task(self):
        account, token = self.create_account_and_get_token()
        comment_data = {"task_id": "507f1f77bcf86cd799439011", "content": "Test comment"}
        with app.test_client() as client:
            response = client.post(
                "/api/comments",
                json=comment_data,
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 404
            assert response.json["code"] == CommentErrorCode.TASK_NOT_FOUND

    def test_get_comment_success(self):
        account, token = self.create_account_and_get_token()
        task_id = self.create_task_and_get_id(account, token)
        comment_data = {"task_id": task_id, "content": "Test comment"}
        with app.test_client() as client:
            create_response = client.post(
                "/api/comments",
                json=comment_data,
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            comment_id = create_response.json["id"]
            get_response = client.get(
                f"/api/comments/{comment_id}",
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            assert get_response.status_code == 200
            assert get_response.json["id"] == comment_id

    def test_get_comments_for_task(self):
        account, token = self.create_account_and_get_token()
        task_id = self.create_task_and_get_id(account, token)
        # Create two comments
        with app.test_client() as client:
            for i in range(2):
                client.post(
                    "/api/comments",
                    json={"task_id": task_id, "content": f"Comment {i}"},
                    headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
                )
            get_response = client.get(
                f"/api/comments?task_id={task_id}",
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            assert get_response.status_code == 200
            assert len(get_response.json) == 2

    def test_update_comment_success(self):
        account, token = self.create_account_and_get_token()
        task_id = self.create_task_and_get_id(account, token)
        comment_data = {"task_id": task_id, "content": "Old content"}
        with app.test_client() as client:
            create_response = client.post(
                "/api/comments",
                json=comment_data,
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            comment_id = create_response.json["id"]
            update_response = client.put(
                f"/api/comments/{comment_id}",
                json={"content": "Updated content"},
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            assert update_response.status_code == 200
            assert update_response.json["content"] == "Updated content"

    def test_delete_comment_success(self):
        account, token = self.create_account_and_get_token()
        task_id = self.create_task_and_get_id(account, token)
        comment_data = {"task_id": task_id, "content": "To be deleted"}
        with app.test_client() as client:
            create_response = client.post(
                "/api/comments",
                json=comment_data,
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            comment_id = create_response.json["id"]
            delete_response = client.delete(
                f"/api/comments/{comment_id}",
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            assert delete_response.status_code == 200
            assert delete_response.json["success"] is True
            # Confirm deletion
            get_response = client.get(
                f"/api/comments/{comment_id}",
                headers={**self.HEADERS, "Authorization": f"Bearer {token}"},
            )
            assert get_response.status_code == 404

    def test_unauthorized_access(self):
        account, token = self.create_account_and_get_token()
        task_id = self.create_task_and_get_id(account, token)
        comment_data = {"task_id": task_id, "content": "Test comment"}
        with app.test_client() as client:
            # No auth header
            response = client.post(
                "/api/comments",
                json=comment_data,
                headers=self.HEADERS,
            )
            assert response.status_code == 401 