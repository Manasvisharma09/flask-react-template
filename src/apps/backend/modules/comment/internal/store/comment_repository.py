from typing import Optional

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from modules.application.repository import ApplicationRepository
from modules.comment.internal.store.comment_model import CommentModel
from modules.logger.logger import Logger


COMMENT_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["task_id", "content", "created_at", "updated_at"],
        "properties": {
            "task_id": {"bsonType": "string"},
            "content": {"bsonType": "string"},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
        },
    }
}


class CommentRepository(ApplicationRepository):
    collection_name = CommentModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index(
            [("task_id", 1), ("created_at", 1)], name="task_id_created_at_index"
        )

        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": COMMENT_VALIDATION_SCHEMA,
            "validationLevel": "strict",
        }

        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(cls.collection_name, validator=COMMENT_VALIDATION_SCHEMA)
            else:
                Logger.error(message=f"OperationFailure occurred for collection comments: {e.details}")
        return True

    @staticmethod
    def create_comment(*, comment_model: CommentModel) -> CommentModel:
        bson_data = comment_model.to_bson()
        result = CommentRepository.collection().insert_one(bson_data)
        comment_model.id = result.inserted_id
        return comment_model

    @staticmethod
    def get_comment_by_id(*, comment_id: str) -> Optional[CommentModel]:
        try:
            object_id = ObjectId(comment_id)
        except Exception:
            return None

        bson_data = CommentRepository.collection().find_one({"_id": object_id})
        if bson_data is None:
            return None

        return CommentModel.from_bson(bson_data=bson_data)

    @staticmethod
    def get_comments_by_task_id(*, task_id: str) -> list[CommentModel]:
        bson_data_list = CommentRepository.collection().find({"task_id": task_id}).sort("created_at", 1)
        return [CommentModel.from_bson(bson_data=bson_data) for bson_data in bson_data_list]

    @staticmethod
    def update_comment(*, comment_id: str, comment_model: CommentModel) -> Optional[CommentModel]:
        try:
            object_id = ObjectId(comment_id)
        except Exception:
            return None

        bson_data = comment_model.to_bson()
        bson_data.pop("_id", None)  # Remove _id from update data

        result = CommentRepository.collection().update_one(
            {"_id": object_id}, {"$set": bson_data}
        )

        if result.matched_count == 0:
            return None

        return CommentRepository.get_comment_by_id(comment_id=comment_id)

    @staticmethod
    def delete_comment(*, comment_id: str) -> bool:
        try:
            object_id = ObjectId(comment_id)
        except Exception:
            return False

        result = CommentRepository.collection().delete_one({"_id": object_id})
        return result.deleted_count > 0 