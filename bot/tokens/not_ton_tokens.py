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


class BnbToken(Token):
    @property
    def id(self) -> str:
        return "bnb"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('BNB')


class TrxToken(Token):
    @property
    def id(self) -> str:
        return "trx"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('TRX')


class BusdToken(Token):
    @property
    def id(self) -> str:
        return "busd"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('BUSD')


class UsdcToken(Token):
    @property
    def id(self) -> str:
        return "usdc"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('USDC')


class UsdtToken(Token):
    @property
    def id(self) -> str:
        return "usdt"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('USDT')


btc_token = BtcToken()
eth_token = EthToken()
bnb_token = BnbToken()
trx_token = TrxToken()
busd_token = BusdToken()
usdc_token = UsdcToken()
usdt_token = UsdtToken()
