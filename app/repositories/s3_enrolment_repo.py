import json
from typing import Any, Union

import boto3

from app.config import settings
from app.domain.entities.enrolment import Enrolment
from app.repositories.enrolment_repo import EnrolmentRepo
from app.utils.random import Random


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3 = boto3.client("s3", **settings.s3_configuration)
        self.enrollment_file = "enrolments/{}.json"

    def is_reference_unique(
        self, ref_hash: str
    ) -> Union[bool, Enrolment]:  # TODO combine with get_enrolment
        """
        Check whether given internal_reference is unique or not
        """
        try:
            self.s3.get_object(
                Key=f"employer_reference/{ref_hash}/enrolment_id.json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
        except Exception:
            return True
        else:
            return False

    def get_data_from_bucket(self, key, bucket):
        try:
            obj = self.s3.get_object(Key=key, Bucket=bucket)
            data = json.loads(obj["Body"].read().decode())
            return data

        except Exception:
            raise Exception("No such data in bucket")

    def save_enrolment(self, enrollment: dict):

        enrl = Enrolment(**enrollment)
        ref_hash = Random.get_str_hash(enrl.internal_reference)

        self.s3.put_object(
            Body=bytes(enrl.enrolment_id, "utf-8"),
            Key=f"employer_reference/{ref_hash}/enrolment_id.json",
            Bucket=settings.ENROLMENT_BUCKET,
        )

        self.s3.put_object(
            Body=bytes(enrl.json(), "utf-8"),
            # Body=bytes(enrl.shared_secret, "utf-8"),
            Key=f"enrolments/{enrl.enrolment_id}.json",
            Bucket=settings.ENROLMENT_BUCKET,
        )

        return enrl

    def post_enrolment(self, enrollment: dict) -> dict:
        """
        Add extra enrolment details
        """
        enrollment_file = self.enrollment_file.format(enrollment["enrolment_id"])
        data = self.get_data_from_bucket(enrollment_file, settings.ENROLMENT_BUCKET)
        data.update(**enrollment)
        self.s3.put_object(
            Body=bytes(json.dumps(data), "utf-8"),
            Key=enrollment_file,
            Bucket=settings.ENROLMENT_BUCKET,
        )
        return data

    def get_enrolment(self, enrolment_id: str):
        print(
            "get_enrolment() enrolment_id, BUCKET",
            enrolment_id,
            settings.ENROLMENT_BUCKET,
        )
        data = self.get_data_from_bucket(
            self.enrollment_file.format(enrolment_id), settings.ENROLMENT_BUCKET
        )
        enrolment = Enrolment(**data)
        return enrolment

    def get_enrolment_status(self, enrolment_id: str, callbacks_list: list):
        total_callbacks = len(callbacks_list["callbacks_list"])
        most_recent_callback = ""
        for row in callbacks_list["callbacks_list"]:
            most_recent_callback = row["received"]

        enrolment = {
            "status": {
                "total_callbacks": str(total_callbacks),
                "most_recent_callback": str(most_recent_callback),
            }
        }
        return enrolment
