import logging


class Field:
    def __init__(self, id: str, source: object):
        self._id = id
        self._parse_source(source)
        self._logger = logging.getLogger('field')

    def _parse_source(self, source):
        self.metadata = source['metadata']
        self.cropInfo = source['cropFenology']
        self.damages = source['damages']
        self.treatments = source['treatments']
        self.irrigations = source['irrigation']
        self.harvests = source['harvest']
        self.baling = source['baling']
        self.heckling = source['heckling']
        self.bbch_stages = source['fenologies']
        self.preparations = source['preparation']
        self.warnings = source['warnings']
        self.yields = source['yields']
        self.application_maps = source['applicationmaps']
        self.statistics = source['statistics']
