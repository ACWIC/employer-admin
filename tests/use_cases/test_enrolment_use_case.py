from datetime import datetime
from unittest import mock
from uuid import uuid4

import boto3

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.enrolment_requests import PostEnrolmentRequest
from app.use_cases.enrolment import PostEnrolment

dummy_key = str(uuid4())
dummy_created = datetime.now()
dummy_enrolment = str(uuid4())
dummy_internal_reference = str(uuid4())


@mock.patch("app.repositories.s3_enrolment_repo.S3EnrolmentRepo.get_data_from_bucket")
def test_post_enrolment_success(mock_get_data):
    """
    when new details of enrolment are updated
    it's success
    """
    repo = mock.Mock(spec=S3EnrolmentRepo)
    repo.is_reference_unique.return_value = True
    repo.s3 = mock.Mock(spec=boto3.client)
    repo.s3.return_value.put_object = {}
    repo.get_enrolment.return_value = {}

    enrolment_data = {
        "enrolment_id": dummy_enrolment,
        "internal_reference": dummy_internal_reference,
        "shared_secret": dummy_key,
        "created": dummy_created,
    }
    mock_get_data.return_value = enrolment_data

    payload = {
        "enrolment_id": dummy_enrolment,
        "course_id": "1",
        "employee_id": "1",
        "employee_contact": "ghorahi-dang",
        "agree_pay_fee": True,
        "employee_info_share": False,
        "employer_endpoint": "",
        "sender_sequence": "1",
    }

    enrolment_return = {**enrolment_data, **payload}
    repo.post_enrolment.return_value = enrolment_return

    request = PostEnrolmentRequest(**payload)
    use_case = PostEnrolment(enrolment_repo=repo)
    response = use_case.execute(request)

    assert response.type == "Success"
    assert response.value == enrolment_return
