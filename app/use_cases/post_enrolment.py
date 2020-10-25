from pydantic import BaseModel

from app.config import settings
from app.repositories.enrolment_repo import EnrolmentRepo
from app.requests.enrolment_requests import PostEnrolmentRequest
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class PostEnrolment(BaseModel):
    enrolment_repo: EnrolmentRepo

    class Config:
        # Pydantic will complain if something (enrolment_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, request: PostEnrolmentRequest):
        try:
            # check if enrolment exists or not
            if not self.enrolment_repo.enrolment_exists(
                request.enrolment_id, bucket=settings.ENROLMENT_BUCKET
            ):
                return ResponseFailure.validation_error(
                    message="VALIDATION_ERROR: enrolment_id "
                    + request.enrolment_id
                    + " is not valid."
                )
            enrolment = self.enrolment_repo.post_enrolment(request.to_dict())
            code = SuccessType.SUCCESS
            message = "SUCCESS: The enrolment has been updated."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment, message=message, type=code)
