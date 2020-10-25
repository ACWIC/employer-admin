from datetime import datetime
from uuid import uuid4

from app.config import settings
from app.domain.entities.callback import Callback


class S3Populate:
    def __init__(self):
        pass
        # Call in S3_enrolmet_repo
        # from app.utils.populate_s3 import S3Populate
        # S3Populate().save_dummy_callbacks(self.s3)
        # return {"callbacks_list": []}

    def save_dummy_callbacks(self, s3):
        enrolment_id = "f6746cec-e4c0-4559-bcb3-2026d68ddfc3"
        callback_id = str(uuid4())
        callback = Callback(
            callback_id=callback_id,
            enrolment_id=enrolment_id,
            shared_secret=str(uuid4()),
            tp_sequence=0,
            received=datetime.strptime(
                "2020-10-05T16:12:48.622351", "%Y-%m-%dT%H:%M:%S.%f"
            ),
            payload={},
        )
        s3.put_object(
            Body=bytes(callback.json(), "utf-8"),
            Key="callbacks/" + enrolment_id + "/" + callback_id + ".json",
            Bucket=settings.CALLBACK_BUCKET,
        )
        print("Dummy Callback#1 created")

        callback_id = str(uuid4())
        callback = Callback(
            callback_id=callback_id,
            enrolment_id=enrolment_id,
            shared_secret=str(uuid4()),
            tp_sequence=0,
            received=datetime.strptime(
                "2020-10-20T16:12:48.622351", "%Y-%m-%dT%H:%M:%S.%f"
            ),
            payload={},
        )
        s3.put_object(
            Body=bytes(callback.json(), "utf-8"),
            Key="callbacks/" + enrolment_id + "/" + callback_id + ".json",
            Bucket=settings.CALLBACK_BUCKET,
        )
        print("Dummy Callback#2 created")

        callback_id = str(uuid4())
        callback = Callback(
            callback_id=callback_id,
            enrolment_id=enrolment_id,
            shared_secret=str(uuid4()),
            tp_sequence=0,
            received=datetime.strptime(
                "2020-10-02T16:12:48.622351", "%Y-%m-%dT%H:%M:%S.%f"
            ),
            payload={},
        )
        s3.put_object(
            Body=bytes(callback.json(), "utf-8"),
            Key="callbacks/" + enrolment_id + "/" + callback_id + ".json",
            Bucket=settings.CALLBACK_BUCKET,
        )
        print("Dummy Callback#3 created")
