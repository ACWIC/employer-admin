from fastapi import APIRouter, HTTPException

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.use_cases import create_enrolment as ce
from app.use_cases import get_callback as gc
from app.use_cases import get_callbacks_list as gcl
from app.use_cases import get_enrolment as ge
from app.use_cases import get_enrolment_status as ges

router = APIRouter()
enrolment_repo = S3EnrolmentRepo()


@router.post("/enrolments")
def create_enrolment(inputs: NewEnrolmentRequest):
    """
    The Employer pre-registers a new Enrolment so callbacks can be received

    The assumption is that the employer generates a unique *enrolment_id*
    in some source system they control (LMS, HRMS, etc),
    and registers it with this microservice.
    This allows the microservice to generate keys,
    and prepare to receive callbacks from the training provider
    about this enrolment.
    """
    use_case = ce.CreateNewEnrolment(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}")
def get_enrolment(enrolment_id: str):
    use_case = ge.GetEnrolmentByID(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/status")
def get_enrolment_status(enrolment_id: str):
    """Return the current status of the given enrolment
    This relies on certain callbacks
    with payloads that describe state-changes in the enrolment.

    * negotiate a state-chart and set of message-types
      that relate to state changes.
    * use these message-types to calculate the current state
    """
    use_case = ges.GetEnrolmentStatus(
        enrolment_repo=enrolment_repo
    )
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/journal")
def get_callbacks_list_for_enrolment(
    enrolment_id: str,
):
    use_case = gcl.GetCallbacksList(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/journal/{callback_id}")
def get_callback_for_enrolment(enrolment_id: str, callback_id):
    """
    Returns callback details for an callback of an enrolment
    """
    use_case = gc.GetCallback(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id, callback_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()
