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
    <p>
    Aged Care Provider (employer) can create a new enrolment in their system.\n
    They do this before they send a message to the Training Provider asking them
    to enrol their staff member as a student.\n
    The reason they do it before is so that, when the Training Provider sends callbacks
    (using the enrolment_id and secret key),\n
    the employer is able to:
    <ul>
      <li>know which enrolment the callback is about (because enrolment_id matches)</li>
      <li>know the right person is making the callback, it's not spam (because they know the key)</li>
    </ul>
    <b>internal_reference</b> a unique, non-empty string for employer_reference.\n
    </p>
    """
    use_case = ce.CreateNewEnrolment(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}")
def get_enrolment(enrolment_id: str):
    """
    <p>
    Aged Care Provider (employer) can view enrolment they posted.\n
    He will get,
    <ol>
      <li><b>enrolment_id</b> identifier for enrolment</li>
      <li><b>shared_secret</b> to recieve callback</li>
      <li><b>internal_reference</b> employer_reference</li>
      <li><b>created</b> date and time when the enrolment was created</li>
    </ol>
    </p>
    """
    use_case = ge.GetEnrolmentByID(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/status")
def get_enrolment_status(enrolment_id: str):
    """
    <p>
    Aged Care Provider (employer) can view current status of the enrolment.\n
    The current status is derived from the callbacks.\n
    In the future we will have various status attributes based on specific types of messages\n
    but that's not designed yet. So for now, some simple attributes saying:
    <ul>
      <li>how many callbacks have been received</li>
      <li>when the most recent callback was received</li>
    </ul>
    </p>
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
    <p>
    Aged Care Provider (employer) can view list of callbacks for an enrolment\n
    Not the callbacks themselves, just a list of:
    <ul>
      <li>date/time it was received</li>
      <li>callback_id</li>
    </ul>
    If there have been 0 callbacks, the list will be empty.
    </p>
    """
    use_case = gcl.GetCallbacksList(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/journal/{callback_id}")
def get_callback_for_enrolment(enrolment_id: str, callback_id):
    """
    <p>
    Aged Care Provider (employer) can view callback details for an enrolment\n
    He will get,
    <ol>
      <li><b>callback_id</b> identifier for callback</li>
      <li><b>enrolment_id</b> identifier for enrolment</li>
      <li><b>shared_secret</b> for verification</li>
      <li><b>received</b> date and time when the callback was received</li>
      <li><b>tp_sequence</b> sequence number from training provider source-system.
      These are used for sorting in the order of sender’s intent.</li>
      <li><b>payload</b> required</li>
    </ol>
    </p>
    """
    use_case = gc.GetCallback(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id, callback_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()
