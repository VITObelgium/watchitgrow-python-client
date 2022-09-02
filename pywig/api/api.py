import logging

import requests
from requests import Response
import json

from pywig.api.error import ApiError
from pywig.api.models.field import Field
from pywig.auth.auth import Auth
from pywig.config import Config


class Api:
    def __init__(self, auth: Auth, env: str = 'prod'):
        """
        Initialize the API object for WatchItGrow
        :param auth: Authentication object containing client information to connect to WIG backend
        :param env: Environment to use (dev, prod). Default is set to prod
        """
        self._auth = auth
        self._config = Config(env).read_config()
        self._base_url = self._config['api']['base']
        self._logger = logging.getLogger('api')

    # ---------------------------------------------------------------------
    #       FIELDS
    # ---------------------------------------------------------------------
    def get_field(self, id: str) -> Field:
        """
        Retrieve the field information for one specific field
        :param id: ID of the field for which to retrieve the information
        :return: Field object containing the detailed field information
        """
        self._logger.debug('Retrieving information for field %s' % id)
        response = self._get('application/databio/fields/%s' % id)
        return Field(id=response['id'], source=response['source'])

    def get_fields(self) -> Field:
        """
        Retrieve all fields linked to the authenticated user
        :return: Field object containing the detailed field information
        """
        self._logger.debug('Retrieving fields')
        response = self._get('application/databio/fields/list?source=metadata,cropFenology')
        fields = []
        for field in response:
            fields.append(Field(id=field['id'], source=field['source']))
        return fields

    # ---------------------------------------------------------------------
    #       UTILS
    # ---------------------------------------------------------------------
    def _get(self, url):
        response = requests.get('%s/%s' % (self._base_url, url), headers=self._get_headers())
        return self._parse_response(response)

    def _parse_response(self, response: Response):
        if response.status_code != 200:
            raise ApiError(message='Could not execute request', response=response)
        else:
            return response.json()

    def _get_headers(self) -> object:
        """
        Create the headers that should be added to each outgoing request to the API
        :return: Object representing the headers for the API request
        """
        return {
            'Authorization': 'Bearer %s' % self._auth.get_token()
        }
