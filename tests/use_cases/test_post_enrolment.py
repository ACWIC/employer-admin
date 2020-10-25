from unittest import mock

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.responses import FailureType, SuccessType
from app.use_cases.post_enrolment import PostEnrolment
from tests.test_data.data_provider import DataProvider


def test_post_enrolment_success():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    repo.is_reference_unique.return_value = True
    repo.post_enrolment.return_value = DataProvider().sample_enrolment
    request = DataProvider().sample_enrolment_request

    use_case = PostEnrolment(enrolment_repo=repo)
    response = use_case.execute(request)

    assert response.type == SuccessType.SUCCESS


def test_post_enrolment_failure():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    repo.is_reference_unique.return_value = True
    request = DataProvider().sample_enrolment_request

    repo.post_enrolment.side_effect = Exception()

    use_case = PostEnrolment(enrolment_repo=repo)
    response = use_case.execute(request)

    assert response.type == FailureType.RESOURCE_ERROR
