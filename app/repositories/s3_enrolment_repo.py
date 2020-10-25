import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment, NewEnrolmentSecret
from app.repositories.enrolment_repo import EnrolmentRepo
from app.utils.error_handling import handle_s3_errors
from app.utils.random import Random


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3 = boto3.client("s3", **settings.s3_configuration)

    def create_enrolment(self, internal_reference: str) -> dict:
        enrolment_id = str(Random.get_uuid())
        shared_secret = str(Random.get_uuid())
        ref_hash = Random.get_str_hash(internal_reference)
        shared_secret_ = {"shared_secret": shared_secret}
        shared_secret_ = NewEnrolmentSecret(**shared_secret_)
        with handle_s3_errors():
            self.s3.put_object(
                Body=bytes(enrolment_id, "utf-8"),
                Key=f"employer_reference/{ref_hash}/enrolment_id.json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
            self.s3.put_object(
                Body=bytes(shared_secret_.json(), "utf-8"),
                Key=f"enrolments/{enrolment_id}.json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
        crete_enrolment_response = {
            "enrolment_id": enrolment_id,
            "shared_secret": shared_secret,
            "ref_hash": ref_hash,
        }
        return crete_enrolment_response

    def post_enrolment(self, extra_details: dict) -> Enrolment:
        with handle_s3_errors():
            obj = self.s3.get_object(
                Key="enrolments/" + extra_details["enrolment_id"] + ".json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
        shared_secret = json.loads(obj["Body"].read().decode())
        extra_details["shared_secret"] = shared_secret["shared_secret"]
        enrolment = Enrolment(**extra_details)
        with handle_s3_errors():
            self.s3.put_object(
                Body=bytes(enrolment.json(), "utf-8"),
                Key="enrolment_request/" + extra_details["enrolment_id"] + ".json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
        return enrolment

    def get_enrolment_shared_secret(self, enrolment_id: str) -> dict:
        with handle_s3_errors():
            obj = self.s3.get_object(
                Key="enrolments/" + enrolment_id + ".json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
        shared_secret = obj["Body"].read().decode()
        response = {"shared_secret": shared_secret}
        return response

    def get_enrolment_request(self, enrolment_id: str) -> Enrolment:
        with handle_s3_errors():
            obj = self.s3.get_object(
                Key="enrolment_request/" + enrolment_id + ".json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
        enrolment = json.loads(obj["Body"].read().decode())
        enrolment = Enrolment(**enrolment)
        return enrolment

    def enrolment_exists(
        self, enrolment_id: str, bucket=settings.ENROLMENT_BUCKET
    ) -> bool:
        try:
            if bucket == settings.ENROLMENT_BUCKET:
                self.s3.get_object(
                    Key=f"enrolments/{enrolment_id}.json",
                    Bucket=settings.ENROLMENT_BUCKET,
                )
            elif bucket == settings.CALLBACK_BUCKET:
                assert "Contents" in self.s3.list_objects(
                    Prefix=f"callbacks/{enrolment_id}/",
                    Bucket=settings.CALLBACK_BUCKET,
                )
            return True
        except Exception:
            return False

    def is_reference_unique(self, internal_reference: str) -> bool:
        ref_hash = Random.get_str_hash(internal_reference)
        try:
            self.s3.get_object(
                Key=f"employer_reference/{ref_hash}/enrolment_id.json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
            return False
        except Exception:
            return True

    def get_callbacks_list(self, enrolment_id: str):
        with handle_s3_errors():
            callbacks_objects_list = self.s3.list_objects(
                Bucket=settings.CALLBACK_BUCKET, Prefix=f"callbacks/{enrolment_id}/"
            )
        callbacks_list = []
        for row in callbacks_objects_list.get("Contents", []):
            with handle_s3_errors():
                obj = self.s3.get_object(
                    Key=row["Key"], Bucket=settings.CALLBACK_BUCKET
                )
            callback = Callback(**json.loads(obj["Body"].read().decode()))
            callbacks_list.append(
                {"callback_id": callback.callback_id, "received": callback.received}
            )
        return {"callbacks_list": callbacks_list}

    def get_enrolment_status(self, enrolment_id: str):
        callbacks_list = self.get_callbacks_list(enrolment_id)
        total_callbacks = len(callbacks_list["callbacks_list"])
        recent_date = ""
        if total_callbacks > 0:
            recent_date = callbacks_list["callbacks_list"][0]["received"]
            for row in callbacks_list["callbacks_list"]:
                if recent_date < row["received"]:
                    recent_date = row["received"]
        enrolment_status = {
            "status": {
                "total_callbacks": str(total_callbacks),
                "most_recent_callback": str(recent_date),
            }
        }
        return enrolment_status

    def get_callback(self, enrolment_id: str, callback_id: str) -> Callback:
        with handle_s3_errors():
            cb_objects = self.s3.list_objects(
                Bucket=settings.CALLBACK_BUCKET, Prefix=f"callbacks/{enrolment_id}/"
            )
        for cb_obj in cb_objects.get("Contents", []):
            with handle_s3_errors():
                obj = self.s3.get_object(
                    Key=cb_obj["Key"], Bucket=settings.CALLBACK_BUCKET
                )
            callback = Callback(**json.loads(obj["Body"].read().decode()))
            if callback.callback_id == callback_id:
                return callback
        raise Exception(f"Callback with callback_id={enrolment_id} does not exist!")
