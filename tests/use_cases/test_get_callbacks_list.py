from unittest import mock

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.responses import FailureType, SuccessType
from app.use_cases.get_callbacks_list import GetCallbacksList
from tests.test_data.data_provider import DataProvider


def test_get_callbacks_list_success():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    repo.enrolment_exists.return_value = True
    repo.get_callbacks_list.return_value = DataProvider().callbacks_list

    use_case = GetCallbacksList(enrolment_repo=repo)
    response = use_case.execute(enrolment_id)

    assert response.type == SuccessType.SUCCESS


def test_get_callbacks_list_failure():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    repo.enrolment_exists.return_value = True

    repo.get_callbacks_list.side_effect = Exception()

    use_case = GetCallbacksList(enrolment_repo=repo)
    response = use_case.execute(enrolment_id)

    assert response.type == FailureType.RESOURCE_ERROR
