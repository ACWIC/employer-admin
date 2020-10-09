import boto3
from typing import Any, Union
from app.config import Config
from app.repositories.enrolment_repo import EnrolmentRepo
from app.domain.entities.enrolment import Enrolment
from app.utils.random import Random


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.params = {
            "aws_access_key_id": Config.S3_ACCESS_KEY_ID,
            "aws_secret_access_key": Config.S3_SECRET_ACCESS_KEY,
            "endpoint_url": Config.S3_ENDPOINT_URL,
        }
        self.s3 = boto3.client("s3", **self.params)

    def save_enrolment(self, enrollment: dict):

        enrl = Enrolment(**enrollment)
        ref_hash = Random.get_str_hash(enrl.internal_reference)

        self.s3.put_object(
            Body=bytes(enrl.enrolment_id, "utf-8"),
            Key=f"employer_reference/{ref_hash}/enrolment_id.json",
            Bucket=Config.ENROLMENT_BUCKET,
        )

        self.s3.put_object(
            Body=bytes(enrl.shared_secret, "utf-8"),
            Key=f"enrolments/{enrl.enrolment_id}.json",
            Bucket=Config.ENROLMENT_BUCKET,
        )

        return enrl

    def get_enrolment(self, enrolment_id: str) -> None:
        pass

    def is_reference_unique(
        self, ref_hash: str
    ) -> Union[bool, Enrolment]:  # TODO combine with get_enrolment
        """
        Check whether given internal_reference is unique or not
        """
        try:
            self.s3.get_object(
                Key=f"employer_reference/{ref_hash}/enrolment_id.json",
                Bucket=Config.ENROLMENT_BUCKET,
            )
        except Exception:
            return True
        else:
            return False
