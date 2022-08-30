import logging

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from pywig.config import Config


class Auth:
    def __init__(self, env: str = 'prod'):
        """
        Initialize the authentication object for WatchItGrow
        :param env: Environment to use (dev, prod). Default is set to prod
        """
        self._config = Config(env).read_config()
        self._client_id = self._config['auth']['client_id']
        self._token_url = self._config['auth']['token_url']
        self.client = LegacyApplicationClient(client_id=self._client_id)
        self._oauth = OAuth2Session(client=self.client)
        self._token = None
        self._logger = logging.getLogger('auth')

    def authenticate_basic(self, username: str, password: str) -> str:
        """
         Authenticate using a username and password
        :param username: Username to use for the authentication
        :param password: Password of the user to authenticate
        """

        self._logger.debug('Authenticating user %s' % username)

        try:
            self._token = self._oauth.fetch_token(token_url=self._token_url,
                                                  username=username, password=password, client_id=self._client_id)[
                'access_token']
        except ValueError as e:
            self._logger.error('Could not authenticate user', exc_info=True)
            raise e

    def get_token(self) -> str:
        return self._token
