from pydantic import BaseModel

from app.repositories.enrolment_repo import EnrolmentRepo
from app.requests.enrolment_requests import PostEnrolmentRequest
from app.responses import ResponseFailure, ResponseSuccess


class PostEnrolment(BaseModel):
    enrolment_repo: EnrolmentRepo

    class Config:
        arbitrary_types_allowed = True

    def execute(self, enrollment: PostEnrolmentRequest):
        try:
            self.enrolment_repo.get_enrolment(enrollment.enrolment_id)
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)
        else:
            try:
                enrollment = self.enrolment_repo.post_enrolment(
                    enrollment=enrollment.dict()
                )
            except Exception as e:
                return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrollment)
