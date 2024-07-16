from abc import ABC, abstractmethod


class Provider(ABC):
    def __init__(self):
        self.username: str = ""
        self.api_key: str = ""
        self.client: object = None
        self.enabled: bool = False

    @abstractmethod
    def get_hardware_id(self, hostname: str):
        pass

    @abstractmethod
    def create(self, hostname: str, ssh_keys: str, no_public: bool):
        pass

    @abstractmethod
    def cancel(self, hostname: str):
        pass

    @abstractmethod
    def edit(self, hardware_id: int, **kwargs):
        pass

    @abstractmethod
    def list_hardware(self):
        pass

    @abstractmethod
    def enable(self):
        self.enabled = True

    @abstractmethod
    def disable(self):
        self.enabled = False
