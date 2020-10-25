from app.requests import ValidRequest


class NewEnrolmentRequest(ValidRequest):
    internal_reference: str


class PostEnrolmentRequest(ValidRequest):
    enrolment_id: str
    course_id: str
    employee_id: str
    employee_contact: str
    agree_pay_fee: bool
    employee_info_share: bool
    employer_endpoint: str
    sender_sequence: str

    def to_dict(self):
        return vars(self)
