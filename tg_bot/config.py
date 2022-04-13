from dataclasses import dataclass
from typing import List
from environs import Env

@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool



@dataclass
class Misc:

    credentials_file: str



@dataclass
class Config:
    tg_bot: TgBot
    misc: Misc


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token = env.str("BOT_TOKEN"),
            admin_ids = list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS")
        ),
        misc=Misc(
            credentials_file = env.str("CREDENTIALS")
        )
    )