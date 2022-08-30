import logging.config
import pathlib

from pywig.api.api import Api
from pywig.api.models.field import Field
from pywig.auth.auth import Auth

logging.config.fileConfig(pathlib.Path(__file__).parent.resolve() / 'logging.conf')


class Wig:
    def __init__(self, env: str = 'prod'):
        self._auth = Auth(env=env)
        self._api = Api(auth=self._auth, env=env)

    def authenticate_basic(self, username: str, password: str):
        self._auth.authenticate_basic(username=username, password=password)

    def get_field(self, id) -> Field:
        return self._api.get_field(id=id)
