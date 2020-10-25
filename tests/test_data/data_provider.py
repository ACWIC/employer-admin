import datetime

from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment
from app.requests.enrolment_requests import PostEnrolmentRequest
from app.utils.random import Random


class DataProvider:
    sample_enrolment: Enrolment
    sample_enrolment_dict: dict
    sample_callback: Callback
    sample_callback_dict: dict

    sample_enrolment_request: PostEnrolmentRequest
    sample_enrolment_request_dict: dict

    internal_reference = "ref1"
    sample_uuid = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    ref_hash = Random.get_str_hash(internal_reference)
    enrolment_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    callback_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    shared_secret = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    course_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    employee_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    date_time_str = "2018-06-29 08:15:27.243860"
    received = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
    crete_enrolment_response = {
        "enrolment_id": sample_uuid,
        "shared_secret": sample_uuid,
        "ref_hash": ref_hash,
    }
    enrolment_status = {
        "status": {
            "total_callbacks": "1",
            "most_recent_callback": str(received),
        }
    }
    callbacks_list = {
        "callbacks_list": [{"callback_id": callback_id, "received": received}]
    }

    def __init__(self):
        self.sample_enrolment = Enrolment(
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            course_id=self.course_id,
            employee_id=self.employee_id,
            employee_contact="abc",
            agree_pay_fee=True,
            employee_info_share=True,
            employer_endpoint="abc",
            sender_sequence="abc",
        )
        self.sample_enrolment_dict = vars(self.sample_enrolment)

        self.sample_callback = Callback(
            callback_id=self.callback_id,
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            tp_sequence=0,
            received=self.received,
            payload={},
        )
        self.sample_callback_dict = vars(self.sample_callback)

        self.sample_enrolment_request = PostEnrolmentRequest(
            enrolment_id=self.enrolment_id,
            course_id=self.course_id,
            employee_id=self.employee_id,
            employee_contact="abc",
            agree_pay_fee=True,
            employee_info_share=True,
            employer_endpoint="abc",
            sender_sequence="abc",
        )
        self.sample_enrolment_request_dict = vars(self.sample_enrolment_request)
