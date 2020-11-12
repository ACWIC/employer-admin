from app.requests.enrolment_requests import NewEnrolmentRequest
from tests.test_data.data_provider import DataProvider


def test_new_enrolment_reques():
    enrolment = NewEnrolmentRequest(
        internal_reference=DataProvider().internal_reference,
    )

    assert enrolment.internal_reference == DataProvider().internal_reference
