from abc import ABC, abstractmethod

from core.logger import logger


class AbstractFile(ABC):
    _host: str
    _key: str
    _key_passphrase: str
    _port: int
    _user: str

    @abstractmethod
    def upload(self, *args, **kwargs):
        pass

    @abstractmethod
    def download(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass


class AbstractStorage(ABC):
    _host: str
    _key: str
    _key_passphrase: str
    _port: int
    _user: str
