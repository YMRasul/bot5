from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    admin_ids: list
    superuser: int


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None):
    conf = Config(
        tg_bot=TgBot(
            token='5240442552:AAGQtUhRoxZAiKBSvHgg1nNdr1U43Vp8LkQ',
            admin_ids=list((139204666,34)),
            superuser=139204666
        )
    )
    return conf

