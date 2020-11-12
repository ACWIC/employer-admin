from app.domain.entities.enrolment import Enrolment, NewEnrolment, NewEnrolmentSecret
from tests.test_data.data_provider import DataProvider


def test_enrolment_init():
    enrolment = Enrolment(
        enrolment_id=DataProvider().enrolment_id,
        shared_secret=DataProvider().shared_secret,
        internal_reference=DataProvider().internal_reference,
        created=DataProvider().created,
    )

    assert enrolment.enrolment_id == DataProvider().enrolment_id
    assert enrolment.shared_secret == DataProvider().shared_secret
    assert enrolment.internal_reference == DataProvider().internal_reference
    assert enrolment.created == DataProvider().created


def test_new_enrolment_init():
    enrolment = NewEnrolment(enrolment_id=DataProvider().enrolment_id)

    assert enrolment.enrolment_id == DataProvider().enrolment_id


def test_new_enrolment_secret_init():
    enrolment = NewEnrolmentSecret(
        shared_secret=DataProvider().shared_secret,
    )

    assert enrolment.shared_secret == DataProvider().shared_secret
