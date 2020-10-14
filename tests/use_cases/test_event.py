from datetime import datetime
from unittest.mock import patch

from app.domain.entities.enrolment import Enrolment
from app.repositories.s3_callback_repo import S3CallbackRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.use_cases.event import EventDetails


@patch("app.repositories.s3_enrolment_repo.S3EnrolmentRepo.get_enrolment")
@patch("app.repositories.s3_callback_repo.S3CallbackRepo.get_event_details")
def test_get_event_detail(get_event_details, get_enrolment):

    enrolment_repo = S3EnrolmentRepo()
    callback_repo = S3CallbackRepo()
    use_case = EventDetails(enrolment_repo=enrolment_repo, callback_repo=callback_repo)
    assert use_case.enrolment_repo == enrolment_repo
    assert use_case.callback_repo == callback_repo

    get_enrolment.return_value = Enrolment(
        enrolment_id="1",
        created=datetime.now(),
        shared_secret="2323",
        internal_reference="wf2323",
    )
    get_event_details.return_value = {}
    response = use_case.execute(enrolment_id="e1", event_id="a1")
    assert response.type == "Success"
    print("tested")
