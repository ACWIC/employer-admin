import abc


class EnrolmentRepo(abc.ABC):
    @abc.abstractmethod
    def save_enrolment(self, enrolment_id) -> None:
        pass
