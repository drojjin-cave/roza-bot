from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    admins_roza: list
    admin_channel: str

@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            admins_roza=[int(id) for id in env.str("ADMINS_ROZA").split()],
            admin_channel=env.str("ADMIN_CHANNEL")
        )
    )

settings = get_settings('input.txt')
