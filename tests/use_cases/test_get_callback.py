from unittest import mock

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.responses import FailureType, SuccessType
from app.use_cases.get_callback import GetCallback
from tests.test_data.data_provider import DataProvider


def test_get_callback_success():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    callback_id = DataProvider().callback_id
    repo.enrolment_exists.return_value = True
    repo.get_callback.return_value = DataProvider().sample_enrolment

    use_case = GetCallback(enrolment_repo=repo)
    response = use_case.execute(enrolment_id, callback_id)

    assert response.type == SuccessType.SUCCESS


def test_get_callback_not_exists():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    callback_id = DataProvider().callback_id
    repo.enrolment_exists.return_value = False
    repo.get_callback.return_value = DataProvider().sample_enrolment

    use_case = GetCallback(enrolment_repo=repo)
    response = use_case.execute(enrolment_id, callback_id)

    assert response.type == FailureType.VALIDATION_ERROR


def test_get_callback_failure():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    callback_id = DataProvider().callback_id
    repo.enrolment_exists.return_value = True

    repo.get_callback.side_effect = Exception()

    use_case = GetCallback(enrolment_repo=repo)
    response = use_case.execute(enrolment_id, callback_id)

    assert response.type == FailureType.RESOURCE_ERROR
