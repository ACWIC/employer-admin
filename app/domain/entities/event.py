from pydantic import BaseModel


class Event(BaseModel):
    event_id: str
    enrolment_id: str
