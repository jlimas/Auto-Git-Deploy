import abc


class Provider(abc.ABC):
    @abc.abstractmethod
    def get_url_from_json_payload(self):
        pass
