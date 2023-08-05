CRYPTO_PAY_COMMISSION = 0.03  # 3%
CRYPTO_PAY_MIN_WITHDRAW = 1  # USD
FOR_STABLE_COINS = 5  # USD

USDC_MIN_WITHDDRAW = 1.51
USDC_FEE = 1.5

BUSD_MIN_WITHDDRAW = 1.51
BUSD_FEE = 1.5

USDT_MIN_WITHDDRAW = 2.5
USDT_FEE = 1.5

TRX_MIN_WITHDDRAW = 25
TRX_FEE = 5

BNB_MIN_WITHDDRAW = 0.0055
BNB_FEE = 0.0045

ETH_MIN_WITHDDRAW = 0.0035
ETH_FEE = 0.0025

BTC_MIN_WITHDDRAW = 0.0013
BTC_FEE = 0.0003

TON_MIN_WITHDDRAW = 0.1005
TON_FEE = 0.1


# class CryptoCoin:
#     def __init__(self, min_withdraw, fee):
#         self.min_withdraw = min_withdraw
#         self.fee = fee
#
#     def min_dep_including_fees_crypto_bot(self):
#         return (self.min_withdraw + self.fee) / (1.02 + CRYPTO_PAY_COMMISSION)
#
#
# # STABLE COINS
#
# class USDC(CryptoCoin):
#     def __init__(self):
#         super().__init__(min_withdraw=USDC_MIN_WITHDDRAW, fee=USDC_FEE)
#
#     def min_dep(self):
#         return max(self.min_dep_including_fees_crypto_bot(), 5)
#
#
# class BUSD(CryptoCoin):
#     def __init__(self):
#         super().__init__(min_withdraw=BUSD_MIN_WITHDDRAW, fee=BUSD_FEE)
#
#     def min_dep(self):
#         return max(self.min_dep_including_fees_crypto_bot(), 5)
#
#
# class USDT(CryptoCoin):
#     def __init__(self):
#         super().__init__(min_withdraw=USDT_MIN_WITHDDRAW, fee=USDT_FEE)
#
#     def min_dep(self):
#         return max(self.min_dep_including_fees_crypto_bot(), 5)
#
#
# # COINS
#
# class TRX(CryptoCoin):
#     def __init__(self):
#         super().__init__(min_withdraw=TRX_MIN_WITHDDRAW, fee=TRX_FEE)
#
#     def min_dep(self, conversion_rate):
#         return max(self.min_dep_including_fees_crypto_bot(), CRYPTO_PAY_MIN_WITHDRAW * conversion_rate)
#
#
# class BNB(CryptoCoin):
#     def __init__(self):
#         super().__init__(min_withdraw=BNB_MIN_WITHDDRAW, fee=BNB_FEE)
#
#     def min_dep(self, conversion_rate):
#         return max(self.min_dep_including_fees_crypto_bot(), CRYPTO_PAY_MIN_WITHDRAW * conversion_rate)
#
#
# class ETH(CryptoCoin):
#     def __init__(self):
#         super().__init__(min_withdraw=ETH_MIN_WITHDDRAW, fee=ETH_FEE)
#
#     def min_dep(self, conversion_rate):
#         return max(self.min_dep_including_fees_crypto_bot(), CRYPTO_PAY_MIN_WITHDRAW * conversion_rate)
#
#
# class BTC(CryptoCoin):
#     def __init__(self):
#         super().__init__(min_withdraw=BTC_MIN_WITHDDRAW, fee=BTC_FEE)
#
#     def min_dep(self, conversion_rate):
#         return max(self.min_dep_including_fees_crypto_bot(), CRYPTO_PAY_MIN_WITHDRAW * conversion_rate)
#
#
# class TON(CryptoCoin):
#     def __init__(self):
#         super().__init__(min_withdraw=TON_MIN_WITHDDRAW, fee=TON_FEE)
#
#     def min_dep(self, conversion_rate):
#         return max(self.min_dep_including_fees_crypto_bot(), CRYPTO_PAY_MIN_WITHDRAW * conversion_rate)
#
#
# MIN_DEP_FOR_CRYPTO_BOT_COIN = {
#     'TON': TON(),
#     'USDC': USDC(),
#     'BUSD': BUSD(),
#     'USDT': USDT(),
#     'TRX': TRX(),
#     'BNB': BNB(),
#     'ETH': ETH(),
#     'BTC': BTC(),
# }
