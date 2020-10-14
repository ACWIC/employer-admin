from datetime import datetime

from pydantic import BaseModel


class EventDetail(BaseModel):
    event_id: str
    enrolment_id: str
    received: datetime
    key: str
    tp_sequence: int
    payload: dict
