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
    Aged Care Provider (employer) can create a new enrolment in their system.\n
    They do this before they send a message to the Training Provider asking them
    to enrol their staff member as a student.\n
    The reason they do it before is so that, when the Training Provider sends callbacks
    (using the enrolment_id and secret key),\n
    the employer is able to:
    - know which enrolment the callback is about (because enrolment_id matches)
    - know the right person is making the callback, it's not spam (because they know the key)\n\n
    **internal_reference** a unique, non-empty string for employer_reference.\n
    """
    use_case = ce.CreateNewEnrolment(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}")
def get_enrolment(enrolment_id: str):
    """
    Aged Care Provider (employer) can view enrolment they posted.\n
    He will get,
    - **enrolment_id** identifier for enrolment
    - **shared_secret** to recieve callback
    - **internal_reference** employer_reference
    - **created** date and time when the enrolment was created
    """
    use_case = ge.GetEnrolmentByID(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/status")
def get_enrolment_status(enrolment_id: str):
    """
    Aged Care Provider (employer) can view current status of the enrolment.\n
    The current status is derived from the callbacks.\n
    In the future we will have various status attributes based on specific types of messages\n
    but that's not designed yet. So for now, some simple attributes saying:
    - how many callbacks have been received
    - when the most recent callback was received
    """
    use_case = ges.GetEnrolmentStatus(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/journal")
def get_callbacks_list_for_enrolment(
    enrolment_id: str,
):
    """
    Aged Care Provider (employer) can view list of callbacks for an enrolment\n
    Not the callbacks themselves, just a list of:
    - **date/time** it was received
    - **callback_id** unique identifier for callback\n\n
    If there have been 0 callbacks, the list will be empty.
    """
    use_case = gcl.GetCallbacksList(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/journal/{callback_id}")
def get_callback_for_enrolment(enrolment_id: str, callback_id):
    """
    Aged Care Provider (employer) can view callback details for an enrolment\n
    He will get,
    - **callback_id** identifier for callback
    - **enrolment_id** identifier for enrolment
    - **shared_secret** for verification
    - **received** date and time when the callback was received
    - **tp_sequence** sequence number from training provider source-system.
      These are used for sorting in the order of sender’s intent.
    - **payload** required
    """
    use_case = gc.GetCallback(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id, callback_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()
