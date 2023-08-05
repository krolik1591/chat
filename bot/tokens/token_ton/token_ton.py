from bot.consts.balance import TON_FUNDS_ICON
from bot.tokens.CryptoPay import CryptoPay
from bot.tokens.base_token import InsufficientFunds, Token
from bot.tokens.token_ton.tonwrapper.tonwrapper import TonWrapper
from bot.consts import crypto_pay_bot_const as consts


class TonToken(Token):
    @property
    def id(self) -> str:
        return "ton"

    @property
    def icon(self) -> str:
        return TON_FUNDS_ICON

    async def min_dep(self):
        min_dep_including_fees = (consts.TON_MIN_WITHDDRAW + consts.TON_FEE) / (1.02 + consts.CRYPTO_PAY_COMMISSION)
        return max(min_dep_including_fees, consts.CRYPTO_PAY_MIN_WITHDRAW * (await self.get_price()))

    async def get_price(self) -> float:
        return await CryptoPay.INSTANCE.get_price('TON')

    async def can_transfer(self, withdraw_amount):
        master_wallet = TonWrapper.INSTANCE.master_wallet
        master_balance_nanoton = await master_wallet.get_balance()

        withdraw_amount_ton = await self.from_gametokens(withdraw_amount)
        withdraw_amount_nanoton = withdraw_amount_ton * 1e9

        if withdraw_amount_nanoton >= master_balance_nanoton:
            raise InsufficientFunds()

        return True

    async def transfer(self, withdraw_address, withdraw_amount, msg):
        master_wallet = TonWrapper.INSTANCE.master_wallet
        withdraw_amount_ton = await self.from_gametokens(withdraw_amount)
        await master_wallet.transfer_ton(withdraw_address, withdraw_amount_ton, msg)
        return withdraw_amount_ton  # todo return tx hash or something

    def withdraw_commission(self):
        return consts.TON_FEE


ton_token = TonToken()
