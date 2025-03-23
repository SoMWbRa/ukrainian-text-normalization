from abc import ABC, abstractmethod
from typing import Tuple, List


class AbstractNormalizer(ABC):
    @staticmethod
    @abstractmethod
    def name() -> str:
        """Returns the name of the normalizer."""
        pass

    @staticmethod
    @abstractmethod
    def normalize(text: str) -> Tuple[str, List[str], List[str]]:
        """Normalizes the text and returns it with a list of warnings and errors."""
        pass
