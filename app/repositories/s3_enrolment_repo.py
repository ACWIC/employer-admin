import os
import uuid
from datetime import datetime
from typing import Any

import boto3

from app.domain.entities.enrolment import Enrolment
from app.repositories.enrolment_repo import EnrolmentRepo

connection_data = {
    "aws_access_key_id": os.environ.get(
        "S3_ACCESS_KEY_ID",
    )
    or None,
    "aws_secret_access_key": os.environ.get(
        "S3_SECRET_ACCESS_KEY",
    )
    or None,
    "endpoint_url": os.environ.get(
        "S3_ENDPOINT_URL", "https://s3.us-east-1.amazonaws.com"
    ),
}


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3 = boto3.client("s3", **connection_data)

    def save_enrolment(self, enrolment_id: str):

        enrl = Enrolment(
            enrolment_id=enrolment_id,
            key=str(uuid.uuid4()),  # random GUID
            created=datetime.now(),  # check the clock
        )

        self.s3.put_object(
            Body=bytes(enrl.json(), "utf-8"),
            Key=f"{enrl.enrolment_id}.json",
            Bucket=os.environ["ENROLMENT_BUCKET"],
        )

        return enrl

    def get_enrolment(self, enrolment_id: str):
        return {}
