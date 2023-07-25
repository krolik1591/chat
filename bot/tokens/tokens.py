from bot.tokens.base_token import Token
from bot.tokens.not_ton_tokens import btc_token, eth_token
from bot.tokens.token_ton.token_ton import ton_token

TOKENS = {
    ton_token.id: ton_token,
    btc_token.id: btc_token,
    eth_token.id: eth_token,
}


async def get_token_by_id(token_id) -> Token:
    return TOKENS[token_id]

