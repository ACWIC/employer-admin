from pydantic import BaseModel

from app.config import settings
from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class GetCallback(BaseModel):
    enrolment_repo: EnrolmentRepo

    class Config:
        arbitrary_types_allowed = True

    def execute(self, enrolment_id: str, callback_id: str):
        try:
            # check if enrolment exists or not
            if not self.enrolment_repo.enrolment_exists(
                enrolment_id, bucket=settings.ENROLMENT_BUCKET
            ):
                return ResponseFailure.build_from_validation_error(
                    message="enrolment_id " + enrolment_id + " is not valid."
                )
            enrolment = self.enrolment_repo.get_callback(
                enrolment_id=enrolment_id, callback_id=callback_id
            )
            code = SuccessType.SUCCESS
            message = "The callback has been fetched."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment, message=message, type=code)
