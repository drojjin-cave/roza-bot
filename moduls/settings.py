from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    admins_vpn: list


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
            admins_vpn=[int(id) for id in env.str("ADMINS_VPN").split()]
        )
    )

settings = get_settings('input.txt')
