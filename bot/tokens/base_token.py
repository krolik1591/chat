import warnings
from abc import ABC


class Token(ABC):
    @property
    def token_id(self) -> str:
        warnings.warn("Deprecated property token_id use id instead", category=DeprecationWarning, stacklevel=2)
        return self.id

    @property
    def id(self) -> str:
        raise NotImplemented

    @property
    def icon(self) -> str:
        raise NotImplemented

    async def get_price(self) -> float:
        raise NotImplemented
