from pydantic import BaseModel

from app.config import settings
from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class GetEnrolmentStatus(BaseModel):
    enrolment_repo: EnrolmentRepo

    class Config:
        arbitrary_types_allowed = True

    def execute(self, enrolment_id: str):
        try:
            # check if enrolment exists or not
            if not self.enrolment_repo.enrolment_exists(
                enrolment_id, bucket=settings.ENROLMENT_BUCKET
            ):
                return ResponseFailure.build_from_validation_error(
                    message="enrolment_id " + enrolment_id + " is not valid."
                )
            enrolment_status = self.enrolment_repo.get_enrolment_status(
                enrolment_id=enrolment_id,
            )
            code = SuccessType.SUCCESS
            message = "Enrolment status has been fetched."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment_status, message=message, type=code)
