import logging
import json


class Field:
    def __init__(self, id: str, source: object):
        self._id = id
        self._parse_source(source)
        self._logger = logging.getLogger('field')

    def _parse_source(self, source):
        self.metadata = source['metadata']
        self.cropInfo = source['cropFenology']
        self.damages = source['damages'] if hasattr(source, 'damages') else None
        self.treatments = source['treatments'] if hasattr(source, 'treatments') else None
        self.irrigations = source['irrigation'] if hasattr(source, 'irrigation') else None
        self.harvests = source['harvest'] if hasattr(source, 'harvest') else None
        self.baling = source['baling'] if hasattr(source, 'baling') else None
        self.heckling = source['heckling'] if hasattr(source, 'heckling') else None
        self.bbch_stages = source['fenologies'] if hasattr(source, 'fenologies') else None
        self.preparations = source['preparation'] if hasattr(source, 'preparation') else None
        self.warnings = source['warnings'] if hasattr(source, 'warnings') else None
        self.yields = source['yields'] if hasattr(source, 'yields') else None
        self.application_maps = source['applicationmaps'] if hasattr(source, 'applicationmaps') else None
        self.statistics = source['statistics'] if hasattr(source, 'statistics') else None
        self.meteo = source['meteo'] if hasattr(source, 'meteo') else None

    def to_json(self):
        field = dict()
        field['metadata'] = self.metadata
        field['cropInfo'] = self.cropInfo
        field['damages'] = self.damages
        field['treatments'] = self.treatments
        field['irrigations'] = self.irrigations
        field['harvests'] = self.harvests
        field['baling'] = self.baling
        field['heckling'] = self.heckling
        field['bbch_stages'] = self.bbch_stages
        field['preparations'] = self.preparations
        field['warnings'] = self.warnings
        field['yields'] = self.yields
        field['application_maps'] = self.application_maps
        field['statistics'] = self.statistics
        return field

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)

    def __repr__(self):
        return self.__str__()
