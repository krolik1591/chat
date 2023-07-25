from bot.tokens.CryptoPay import CryptoPay
from bot.tokens.base_token import Token


class BtcToken(Token):
    @property
    def id(self) -> str:
        return "btc"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('BTC')


class EthToken(Token):
    @property
    def id(self) -> str:
        return "eth"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('ETH')


btc_token = BtcToken()
eth_token = EthToken()
