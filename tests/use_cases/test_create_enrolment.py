from unittest import mock

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.responses import FailureType, SuccessType
from app.use_cases.create_enrolment import CreateNewEnrolment
from tests.test_data.data_provider import DataProvider


def test_create_enrolment_success():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    internal_reference = DataProvider().internal_reference
    repo.is_reference_unique.return_value = True
    repo.create_enrolment.return_value = DataProvider().crete_enrolment_response
    request = NewEnrolmentRequest(internal_reference=internal_reference)

    use_case = CreateNewEnrolment(enrolment_repo=repo)
    response = use_case.execute(request)

    assert response.type == SuccessType.CREATED


def test_create_enrolment_failure():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    internal_reference = DataProvider().internal_reference
    repo.is_reference_unique.return_value = True
    request = NewEnrolmentRequest(internal_reference=internal_reference)

    repo.create_enrolment.side_effect = Exception()

    use_case = CreateNewEnrolment(enrolment_repo=repo)
    response = use_case.execute(request)

    assert response.type == FailureType.RESOURCE_ERROR
