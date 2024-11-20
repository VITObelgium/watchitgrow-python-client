import logging
from typing import List

import requests
from requests import Response
import json

from shapely.geometry import shape

from pywig.api.error import ApiError
from pywig.api.models.field import Field
from pywig.api.models.meteostat import MeteoStat
from pywig.auth.auth import Auth
from pywig.config import Config


class Api:
    def __init__(self, auth: Auth, env: str = 'prod'):
        """Initialize the API object for WatchItGrow

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
        """Retrieve the field information for one specific field

        :param id: ID of the field for which to retrieve the information
        :return: Field object containing the detailed field information
        """
        self._logger.debug('Retrieving information for field %s' % id)
        response = self._get('databio/application/databio/fields/%s' % id)
        return Field(id=response['id'], source=response['source'])

    def get_fields(self) -> List[Field]:
        """Retrieve all fields linked to the authenticated user

        :return: Field object containing the detailed field information
        """
        self._logger.debug('Retrieving fields')
        response = self._get('databio/application/databio/fields/list?source=metadata,cropFenology')
        fields = []
        for field in response:
            fields.append(Field(id=field['id'], source=field['source']))
        return fields

    # ---------------------------------------------------------------------
    #       METEO
    # ---------------------------------------------------------------------
    def get_meteo_data(self, geometry: dict, start_date: str, end_date: str, key: str) -> List[MeteoStat]:
        """Retrieve the meteo statistics from the API

        :param geometry: Geometry for which to retrieve the statistics
        :param start_date: Start date for the statistics
        :param end_date: End date for the statistics
        :param key: Key representing the type of statistic that should be requested (AVERAGE_TEMPERATURE,
        MAXIMUM_TEMPERATURE, MINIMUM_TEMPERATURE, RAINFALL)
        :return: A list of statistics representing the meteo information that was requested
        """
        self._logger.debug(f'Requesting KMI data for {key} with a range from {start_date} to {end_date}')
        bbox = shape(geometry).bounds
        response = self._post(f'/kmi/{key.upper()}', {
            'interval': 1,
            'minX': bbox[0],
            'minY': bbox[1],
            'maxX': bbox[2],
            'maxY': bbox[3],
            'range': {
                'gte': start_date,
                'lte': end_date
            }
        })
        if 'aggregations' in response and 'date_histogram#aggregatedTimeSeries' in response['aggregations']:
            if len(response['aggregations']['date_histogram#aggregatedTimeSeries']['buckets']) > 0:
                if ('sum#aggResult' in response['aggregations']['date_histogram#aggregatedTimeSeries']['buckets'][0]):
                    return list(map(lambda x: MeteoStat(date=x['key_as_string'], value=x['sum#aggResult']['value']),
                            response['aggregations']['date_histogram#aggregatedTimeSeries']['buckets']))
                else:
                    return list(map(lambda x: MeteoStat(date=x['key_as_string'], value=x['avg#aggResult']['value']),
                                    response['aggregations']['date_histogram#aggregatedTimeSeries']['buckets']))
            else:
                raise Exception('No data found')
        else:
            raise Exception('Could not parse the meteo response from the API')

    # ---------------------------------------------------------------------
    #       UTILS
    # ---------------------------------------------------------------------
    def _get(self, url) -> object:
        """Execute a GET request to the WIG API

        :param url: URL to which the post request should be made
        :return: JSON body of the response
        """
        response = requests.get('%s/%s' % (self._base_url, url), headers=self._get_headers())
        return self._parse_response(response)

    def _post(self, url, body) -> object:
        """Execute a POST request to the WIG API

        :param url: URL to which the post request should be made
        :param body: Body of the post request
        :return: JSON body of the response
        """
        response = requests.post('%s/%s' % (self._base_url, url), json=body, headers=self._get_headers())
        return self._parse_response(response)

    def _parse_response(self, response: Response) -> object:
        """Parse the response coming back from the API

        :param response: Response object
        :raises ApiError: Error that is raised whenever the API does not send a 200 response
        :return: JSON body of the response
        """
        if response.status_code != 200:
            raise ApiError(message='Could not execute request to the API: ' + response.status_code + ' ' + response.reason, response=response)
        else:
            return response.json()

    def _get_headers(self) -> object:
        """Create the headers that should be added to each outgoing request to the API

        :return: Object representing the headers for the API request
        """
        return {
            'Authorization': 'Bearer %s' % self._auth.get_token()
        }
