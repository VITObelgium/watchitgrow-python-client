import logging

from requests import Response

class ApiError(Exception):
    """
    Raised if the WIG API returned an error
    """
    def __init__(self, message, response: Response):
        self._logger = logging.getLogger('api')
        self.message = '%s (status: %d): %s' % (message, response.status_code, response.text)
        self._logger.error(message)
        super().__init__(message)
