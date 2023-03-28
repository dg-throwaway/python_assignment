#!/usr/bin/env python3
"""Add env/configs and stuff here"""
from dotenv import load_dotenv, dotenv_values


load_dotenv()


class BaseEnv:
    """Enforced environment variable manager: add environment variables here
    along with the ones in .env to get code completion.
    App will also throw an error if there is a mismatch between .env and this class
    """

    VANTAGE_API_KEY: str
    DATABASE_CONNECTIONSTRING: str

    def __init__(self):
        declared_envs = self.__annotations__.keys()
        for k, v in dotenv_values().items():
            if k not in declared_envs:
                raise Exception("ERROR: Environment variables mismatch.")
            setattr(self, k, v)


Env = BaseEnv()
