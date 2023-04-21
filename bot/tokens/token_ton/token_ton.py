from bot.texts import TON_FUNDS_ICON
from bot.tokens.base_token import Token


class TonToken(Token):
    @property
    def id(self) -> str:
        return "ton"

    @property
    def icon(self) -> str:
        return TON_FUNDS_ICON

    async def get_price(self) -> float:
        # todo calc from usd price
        return 100

    async def to_gametoken(self, amount_ton: float) -> float:
        return amount_ton * await self.get_price()


ton_token = TonToken()
