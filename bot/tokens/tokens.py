from bot.tokens.base_token import Token
from bot.tokens.token_ton.token_ton import ton_token

TOKENS = {
    ton_token.id: ton_token
}


async def get_token_by_id(token_id) -> Token:
    return TOKENS[token_id]

