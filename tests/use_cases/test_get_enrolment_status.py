from unittest import mock

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.responses import FailureType, SuccessType
from app.use_cases.get_enrolment_status import GetEnrolmentStatus
from tests.test_data.data_provider import DataProvider


def test_get_callback_success():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    repo.enrolment_exists.return_value = True
    repo.get_enrolment_status.return_value = DataProvider().sample_callback

    use_case = GetEnrolmentStatus(enrolment_repo=repo)
    response = use_case.execute(enrolment_id)

    assert response.type == SuccessType.SUCCESS


def test_get_callback_failure():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    repo.enrolment_exists.return_value = True

    repo.get_enrolment_status.side_effect = Exception()

    use_case = GetEnrolmentStatus(enrolment_repo=repo)
    response = use_case.execute(enrolment_id)

    assert response.type == FailureType.RESOURCE_ERROR
