from bot.tokens.CryptoPay import CryptoPay
from bot.tokens.base_token import Token
from bot.consts import crypto_pay_bot_const as consts


class BtcToken(Token):
    @property
    def id(self) -> str:
        return "btc"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('BTC')

    async def min_dep(self):
        min_dep_including_fees = (consts.BTC_MIN_WITHDDRAW + consts.BTC_FEE) / (1.02 + consts.CRYPTO_PAY_COMMISSION)
        return max(min_dep_including_fees, consts.CRYPTO_PAY_MIN_WITHDRAW / (await self.get_price()))


class EthToken(Token):
    @property
    def id(self) -> str:
        return "eth"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('ETH')

    async def min_dep(self):
        min_dep_including_fees = (consts.ETH_MIN_WITHDDRAW + consts.ETH_FEE) / (1.02 + consts.CRYPTO_PAY_COMMISSION)
        return max(min_dep_including_fees, consts.CRYPTO_PAY_MIN_WITHDRAW / (await self.get_price()))


class BnbToken(Token):
    @property
    def id(self) -> str:
        return "bnb"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('BNB')

    async def min_dep(self):
        min_dep_including_fees = (consts.BNB_MIN_WITHDDRAW + consts.BNB_FEE) / (1.02 + consts.CRYPTO_PAY_COMMISSION)
        return max(min_dep_including_fees, consts.CRYPTO_PAY_MIN_WITHDRAW / (await self.get_price()))


class TrxToken(Token):
    @property
    def id(self) -> str:
        return "trx"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('TRX')

    async def min_dep(self):
        min_dep_including_fees = (consts.TRX_MIN_WITHDDRAW + consts.TRX_FEE) / (1.02 + consts.CRYPTO_PAY_COMMISSION)
        return max(min_dep_including_fees, consts.CRYPTO_PAY_MIN_WITHDRAW / (await self.get_price()))


# STABLE COINS

class BusdToken(Token):
    @property
    def id(self) -> str:
        return "busd"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('BUSD')

    async def min_dep(self):
        min_dep_including_fees = (consts.BUSD_MIN_WITHDDRAW + consts.BUSD_FEE) / (1.02 + consts.CRYPTO_PAY_COMMISSION)
        return max(min_dep_including_fees, consts.FOR_STABLE_COINS)


class UsdcToken(Token):
    @property
    def id(self) -> str:
        return "usdc"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('USDC')

    async def min_dep(self):
        min_dep_including_fees = (consts.USDC_MIN_WITHDDRAW + consts.USDC_FEE) / (1.02 + consts.CRYPTO_PAY_COMMISSION)
        return max(min_dep_including_fees, consts.FOR_STABLE_COINS)


class UsdtToken(Token):
    @property
    def id(self) -> str:
        return "usdt"

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('USDT')

    async def min_dep(self):
        min_dep_including_fees = (consts.USDT_MIN_WITHDDRAW + consts.USDT_FEE) / (1.02 + consts.CRYPTO_PAY_COMMISSION)
        return max(min_dep_including_fees, consts.FOR_STABLE_COINS)


btc_token = BtcToken()
eth_token = EthToken()
bnb_token = BnbToken()
trx_token = TrxToken()
busd_token = BusdToken()
usdc_token = UsdcToken()
usdt_token = UsdtToken()
