import datetime
from typing import List

from pywig.api.api import Api
from pywig.api.models.field import Field
from pywig.api.models.meteostat import MeteoStat
from pywig.auth.auth import Auth


class Wig:
    """
    Class that is used to interact with the WatchItGrow API
    """

    def __init__(self, env: str = 'prod'):
        """Initialise the WIG Python client by specifying the environment to which you want to connect. In this case the
        production environment matches the data that is available in the main application: https://app.watchitgrow.be

        :param env: Environment to which you want to connect to (dev or prod). The default is the production environment
        """
        self._auth = Auth(env=env)
        self._api = Api(auth=self._auth, env=env)

    def authenticate_basic(self, username: str, password: str):
        """Authenticate with WIG using your username and password

        :param username: Username of your WIG account
        :param password: Password of your WIG account
        """
        self._auth.authenticate_basic(username=username, password=password)

    def get_field_details(self, id) -> Field:
        """Retrieve a field based on its ID

        :param id: ID of the field to retrieve
        :return: Field object containing the full field details
        :rtype: Field
        """
        return self._api.get_field(id=id)

    def get_fields(self) -> List[Field]:
        """Retrieve all fields linked to the authenticated user

        :return: List of field objects containing the basic field information
        :rtype: List
        """
        return self._api.get_fields()

    def get_meteo(self, field_id: str, key: str, start_date: datetime.date = None, end_date: datetime.date = None) -> \
    List[MeteoStat]:
        """Retrieve the meteo statistics for the selected field

        :param field_id: ID of the field for which to retrieve the meteo statistics
        :param key: Key that represents what type of meteo information should be fetched. For fields inside of Belgium, the supported keys are (AVERAGE_TEMPERATURE, MAXIMUM_TEMPERATURE, MINIMUM_TEMPERATURE, RAINFALL). For fields outside of Belgium, the supported keys are (TEMPERATURE, RAINFALL).
        :param start_date: The date from where to retrieve the meteo data
        :param end_date: The end date for the meteo data retrieval
        :return: A list of MeteoStat entries
        :rtype: List
        """
        field = self.get_field_details(field_id)
        if field.meteo and key.lower() in field.meteo:
            meteo = list(map(lambda x: MeteoStat(date=x['date'], value=x['value']), field.meteo[key.lower()]))
            if start_date:
                meteo = [x for x in meteo if start_date <= datetime.datetime.strptime(x.date, "%Y-%m-%d").date()]
            if end_date:
                meteo = [x for x in meteo if datetime.datetime.strptime(x.date, "%Y-%m-%d").date() <= end_date]
            return meteo
        elif field.metadata.country == 'Belgium':
            start_date = start_date.isoformat() if start_date else field.metadata['startDate']
            end_date = end_date.isoformat() if end_date else field.metadata['endDate']

            return self._api.get_meteo_data(geometry=field.metadata['geometry'], key=key,
                                            start_date=start_date, end_date=end_date)
        else:
            raise Exception(
                f'Meteo statistic {key} is not supported for this field, only {",".join(field.meteo.keys())}')
