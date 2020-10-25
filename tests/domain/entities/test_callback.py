from app.domain.entities.callback import Callback
from tests.test_data.data_provider import DataProvider


def test_callback_init():
    callback = Callback(
        callback_id=DataProvider().callback_id,
        enrolment_id=DataProvider().enrolment_id,
        shared_secret=DataProvider().shared_secret,
        tp_sequence=0,
        received=DataProvider().received,
        payload={},
    )

    assert callback.callback_id == DataProvider().callback_id
    assert callback.enrolment_id == DataProvider().enrolment_id
    assert callback.shared_secret == DataProvider().shared_secret
    assert callback.tp_sequence == 0
    assert callback.received == DataProvider().received
    assert callback.payload == {}
