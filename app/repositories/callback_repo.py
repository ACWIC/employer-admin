import abc

from app.domain.entities.callback import Callback
from app.domain.entities.event import Event


class CallbackRepo(abc.ABC):
    @abc.abstractmethod
    def save_callback(
        self, enrolment_id: str, key: str, tp_sequence: int, payload: dict
    ) -> Callback:
        """"""

    @abc.abstractmethod
    def get_callbacks_list(self, enrolment_id: str) -> None:
        pass

    @abc.abstractmethod
    def get_event_details(self, enrolment_id: str, event_id: str) -> Event:
        pass
