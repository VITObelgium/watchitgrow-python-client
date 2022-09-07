import logging.config
import pathlib

from pywig.api.api import Api
from pywig.api.models.field import Field
from pywig.api.models.meteostat import MeteoStat
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

    def get_fields(self) -> list[Field]:
        """
        Retrieve all fields linked to the authenticated user
        :return: Field object
        :rtype: Field
        """
        return self._api.get_fields()

    def get_meteo(self, field_id: str, key: str) -> list[MeteoStat]:
        """
        Retrieve the meteo statistics for the selected field
        :param field_id: ID of the field for which to retrieve the meteo statistics
        :param key: Key that represents what type of meteo information should be fetched. For fields inside of Belgium,
        the supported keys are (AVERAGE_TEMPERATURE, MAXIMUM_TEMPERATURE, MINIMUM_TEMPERATURE, RAINFALL). For fields
        outside of Belgium, the supported keys are (TEMPERATURE, RAINFALL).
        :return:
        """
        field = self.get_field(field_id)
        if field.meteo:
            if key.lower() in field.meteo:
                return list(map(lambda x: MeteoStat(date=x['date'], value=x['value']), field.meteo[key.lower()]))
            else:
                raise Exception(
                    f'Meteo statistic {key} is not supported for this field, only {",".join(field.meteo.keys())}')
        else:
            return self._api.get_meteo_data(geometry=field.metadata['geometry'], start_date=field.metadata['startDate'],
                                            end_date=field.metadata['endDate'], key=key)
