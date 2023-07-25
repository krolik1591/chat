from bot.tokens.base_token import Token
from bot.tokens.not_ton_tokens import bnb_token, btc_token, busd_token, eth_token, trx_token, usdc_token, usdt_token
from bot.tokens.token_ton.token_ton import ton_token

TOKENS = {
    ton_token.id: ton_token,
    btc_token.id: btc_token,
    eth_token.id: eth_token,
    bnb_token.id: bnb_token,
    trx_token.id: trx_token,
    busd_token.id: busd_token,
    usdc_token.id: usdc_token,
    usdt_token.id: usdt_token
}


async def get_token_by_id(token_id) -> Token:
    return TOKENS[token_id]

