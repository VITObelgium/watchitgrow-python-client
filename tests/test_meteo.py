import unittest
import json
from unittest import mock

from mocks.mockresponse import MockResponse

from pywig import Wig, Field, MeteoStat
from tests.utils import get_json_fixture


class FieldTestCases(unittest.TestCase):

    @mock.patch('requests.get', side_effect=lambda *args, **kwargs: MockResponse({
        'id': 'foobar',
        'source': {
            'metadata': {},
            'cropFenology': {},
            'meteo': {
                'temperature': [
                    {
                        'date': '2022-01-01',
                        'value': 1337.01
                    }
                ]
            }
        }
    }, 200, None))
    def test_field_meteo_stats(self, mockGet):
        """
        Should correctly pass and process the statistics that are already linked to the field
        :return:
        """
        wig = Wig()
        result = list(map(lambda x: str(x), wig.get_meteo(field_id='foobar', key='temperature')))
        self.assertEqual(json.dumps(result), json.dumps([str(MeteoStat(date='2022-01-01', value=1337.01))]))

    @mock.patch('requests.get', side_effect=lambda *args, **kwargs: MockResponse({
        'id': 'foobar',
        'source': {
            'metadata': {},
            'cropFenology': {},
            'meteo': {
                'foobar': []
            }
        }
    }, 200, None))
    def test_field_meteo_stats_error(self, mockGet):
        """
        Should throw an error whenever statistics are linked to a field, but the key is not part of it
        :return:
        """
        try:
            wig = Wig()
            result = list(map(lambda x: str(x), wig.get_meteo(field_id='foobar', key='temperature')))
            self.assertTrue(False, 'Expected to throw an error, but none were thrown')
        except:
            self.assertTrue(True)

    @mock.patch('requests.post',
                side_effect=lambda *args, **kwargs: MockResponse(get_json_fixture('meteo_response.json'), 200, None))
    @mock.patch('requests.get',
                side_effect=lambda *args, **kwargs: MockResponse({
                    'id': 'foobar',
                    'source': get_json_fixture('field.json')
                }, 200, None))
    def test_field_meteo_request_ok(self, mockPost, mockGet):
        """
        Should send a request to the API for the retrieval of the statistics
        :return:
        """
        wig = Wig()
        result = list(map(lambda x: str(x), wig.get_meteo(field_id='foobar', key='average_temperature')))
        self.assertEqual(248, len(result))

    @mock.patch('requests.post', side_effect=lambda *args, **kwargs: MockResponse({}, 500, "No can do!"))
    @mock.patch('requests.get', side_effect=lambda *args, **kwargs: MockResponse({
        'id': 'foobar',
        'source': get_json_fixture('field.json')
    }, 200, None))
    def test_field_meteo_request_empty(self, mockPost, mockGet):
        """
        Should throw an error when the API returned an empty result
        :return:
        """
        try:
            wig = Wig()
            result = list(map(lambda x: str(x), wig.get_meteo(field_id='foobar', key='average_temperature')))
            self.assertTrue(False, 'Expected to throw an error, but none were thrown')
        except:
            self.assertTrue(True)

    @mock.patch('requests.post', side_effect=lambda *args, **kwargs: MockResponse(None, 500, "No can do!"))
    @mock.patch('requests.get', side_effect=lambda *args, **kwargs: MockResponse({
        'id': 'foobar',
        'source': get_json_fixture('field.json')
    }, 200, None))
    def test_field_meteo_request_nok(self, mockPost, mockGet):
        """
        Should throw an error when the API returned an error code
        :return:
        """
        try:
            wig = Wig()
            result = list(map(lambda x: str(x), wig.get_meteo(field_id='foobar', key='average_temperature')))
            self.assertTrue(False, 'Expected to throw an error, but none were thrown')
        except:
            self.assertTrue(True)
