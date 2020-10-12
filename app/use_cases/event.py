from pydantic import BaseModel

from app.repositories.callback_repo import CallbackRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import ResponseFailure, ResponseSuccess


class EventDetails(BaseModel):
    enrolment_repo: EnrolmentRepo
    callback_repo: CallbackRepo

    class Config:
        arbitrary_types_allowed = True

    def execute(self, enrolment_id: str, event_id: str):
        try:
            self.enrolment_repo.get_enrolment(enrolment_id)
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)
        else:
            try:
                event = self.callback_repo.get_event_details(
                    enrolment_id=enrolment_id, event_id=event_id
                )
            except Exception as e:
                return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=event)
