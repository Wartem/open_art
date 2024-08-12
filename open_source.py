from abc import ABC, abstractmethod

class Source(ABC):

    @abstractmethod
    def download_open_data(self):
        pass

    @abstractmethod
    def unpack_and_create_csv(self):
        pass