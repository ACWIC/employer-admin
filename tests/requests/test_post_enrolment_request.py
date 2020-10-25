from app.requests.enrolment_requests import PostEnrolmentRequest
from tests.test_data.data_provider import DataProvider


def test_post_enrolment_reques():
    enrolment = PostEnrolmentRequest(
        enrolment_id=DataProvider().enrolment_id,
        course_id=DataProvider().course_id,
        employee_id=DataProvider().employee_id,
        employee_contact="abc",
        agree_pay_fee=True,
        employee_info_share=True,
        employer_endpoint="abc",
        sender_sequence="abc",
    )

    assert enrolment.enrolment_id == DataProvider().enrolment_id
    assert enrolment.course_id == DataProvider().course_id
    assert enrolment.employee_id == DataProvider().employee_id
    assert enrolment.employee_contact == "abc"
    assert enrolment.agree_pay_fee is True
    assert enrolment.employee_info_share is True
    assert enrolment.employer_endpoint == "abc"
    assert enrolment.sender_sequence == "abc"
