import warnings
from abc import ABC


class InsufficientFunds(Exception):
    pass


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

    async def from_gametokens(self, amount: float) -> float:
        return amount / await self.get_price()

    async def to_gametokens(self, amount_ton: float) -> float:
        return amount_ton * await self.get_price()

    async def can_transfer(self, withdraw_amount) -> bool:
        raise NotImplemented

    async def transfer(self, withdraw_address, withdraw_amount, msg):
        raise NotImplemented
