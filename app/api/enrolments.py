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
    Aged Care Provider (employer) can create a new enrolment in their system.
    They do this before they send a message to the Training Provider
    asking them to enrol their staff member as a student.
    The reason they do it before is so that,
    when the Training Provider sends callbacks
    (using the enrolment_id and secret key),
    the employer is able to:

    * know which enrolment the callback is about (because enrolment_id matches)
    * know the right person is making the callback,
      it's not spam (because they know the key)

    The **internal_reference** must be provided.
    It is a unique, non-empty string
    used as a cross-reference into the employer's system.
    This is not shared with the Training Provider.
    Instead, the generated enrollment_id becomes
    a privacy-preserving *quiescent* identifier
    used by both sides to reference the enrolment.
    """
    use_case = ce.CreateNewEnrolment(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}")
def get_enrolment(enrolment_id: str):
    """
    Aged Care Provider (employer) can view enrolment they posted.

    The response contains:

    * **enrolment_id** identifier for enrolment
    * **shared_secret** to recieve callback
    * **internal_reference** employer_reference
    * **created** date and time when the enrolment was created

    While the internal_reference was provided
    when the object was created,
    the other attributes were generated by the microservice.
    """
    use_case = ge.GetEnrolmentByID(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/status")
def get_enrolment_status(enrolment_id: str):
    """
    Aged Care Provider (employer) can view current status of the enrolment
    (derived from the callbacks).

    The current implementation simply identifies:

    * how many callbacks have been received
    * when the most recent callback was received

    In the future we will have various status attributes
    based on specific types of message.
    Topics that might be summarised in the status:

    * state of the procurement of training services
      (e.g. not-acknowledged, processing,
      payment-requested, payment-received,
      enrolment-rejected)
    * state of the training service delivery
      (e.g. not-commenced, in-progress,
      completed-passed, completed-failed,
      withdrawn)
    * any certification obtained

    These would be derived from specific messages
    whose semantics would need to be developed and agreed.
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
    Aged Care Provider (employer) can
    view a list of callbacks for an enrolment,
    so they can discover the callbacks
    that have been received.
    An integrated system might use this to
    discover new callbacks (so they can be downloaded
    for processing), using a polling mechanism.

    **Note:** the polling is against their own system
    (this microservice) not the provider's system,
    so it gives the consumer the option
    of operating in a batch-oriented way
    even if the Training Provider systems
    operate with an event paradigm.

    The current implementation returns a list of:

    * **date/time** it was received
    * **callback_id** unique identifier for callback

    If there have been 0 callbacks, the list will be empty.

    Future iterations may contain more data,
    such as the type of the message.
    Filter parameters may also be useful,
    so that users can access lists of events
    of a certain type or within a particular time range.
    """
    use_case = gcl.GetCallbacksList(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/enrolments/{enrolment_id}/journal/{callback_id}")
def get_callback_for_enrolment(enrolment_id: str, callback_id):
    """
    Aged Care Provider (employer) can view callback details for an enrolment.

    This might typically be used as a data source
    for analytics, or an evidenciary process.

    The response contains:

    * **callback_id** identifier for callback
    * **enrolment_id** identifier for enrolment
    * **shared_secret** for verification
    * **received** date and time when the callback was received
    * **tp_sequence** sequence number from training provider source-system.
    * **payload** required

    Note the tp_sequence is a sender-provided key
    that allows the events to be sorted
    in the *order of sender's intent*.
    This means users can recover from jumbling
    caused by vaguries of the network,
    service availability, etc.

    Alternatively, users can sort by their
    own temporal frame of reference
    using the received time stamps.
    """
    use_case = gc.GetCallback(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id, callback_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()
