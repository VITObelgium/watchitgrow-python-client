import logging.config
import pathlib

from pywig.api.api import Api
from pywig.api.models.field import Field
from pywig.auth.auth import Auth

logging.config.fileConfig(pathlib.Path(__file__).parent.resolve() / 'logging.conf')


class Wig:
    """
    Class that is used to interact with the WatchItGrow API
    """
    def __init__(self, env: str = 'prod'):
        """
        Initialise the WIG Python client by specifying the environment to which you want to connect. In this case the
        production environment matches the data that is available in the main application: https://app.watchitgrow.be
        :param env: Environment to which you want to connect to (dev or prod). The default is the production environment
        """
        self._auth = Auth(env=env)
        self._api = Api(auth=self._auth, env=env)

    def authenticate_basic(self, username: str, password: str):
        """
        Authenticate with WIG using your username and password
        :param username: Username of your WIG account
        :param password: Password of your WIG account
        """
        self._auth.authenticate_basic(username=username, password=password)

    def get_field(self, id) -> Field:
        """
        Retrieve a field based on its ID
        :param id: ID of the field to retrieve
        :return: Field object
        :rtype: Field
        """
        return self._api.get_field(id=id)

    def get_fields(self) -> Field:
        """
        Retrieve all fields linked to the authenticated user
        :return: Field object
        :rtype: Field
        """
        return self._api.get_fields()
