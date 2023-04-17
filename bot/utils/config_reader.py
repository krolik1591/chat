from typing import Optional

from pydantic import BaseSettings, validator, SecretStr, RedisDsn


class Settings(BaseSettings):
    bot_token: SecretStr
    fsm_mode: str
    redis: Optional[RedisDsn]
    wallet_seed: str
    admin_chat_id: int
    admin_ids: str

    @validator("admin_ids")
    def is_admin(cls, v: str):
        return v.split(',')

    @validator("wallet_seed")
    def wallet_seed_check(cls, v: str):
        if v.count(' ') != 23:
            raise ValueError("Incorrect wallet_seed. Need 24 words.")
        return v

    @validator("fsm_mode")
    def fsm_type_check(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect fsm_mode. Must be one of: memory, redis")
        return v

    @validator("redis")
    def skip_validating_redis(cls, v, values):
        if values["fsm_mode"] == "redis" and v is None:
            raise ValueError("Redis config is missing, though fsm_type is 'redis'")
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
