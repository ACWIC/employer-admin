from pydantic import BaseModel


class NewEnrolment(BaseModel):
    enrolment_id: str


class NewEnrolmentSecret(BaseModel):
    shared_secret: str

    def to_dict(self):
        return vars(self)


class Enrolment(BaseModel):
    enrolment_id: str
    shared_secret: str
    shared_secret: str
    course_id: str
    employee_id: str
    employee_contact: str
    agree_pay_fee: bool
    employee_info_share: bool
    employer_endpoint: str
    sender_sequence: str

    def to_dict(self):
        return vars(self)
