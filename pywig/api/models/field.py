import json
import logging

from pywig.api.models import JsonObject


class Field(JsonObject):
    def __init__(self, id: str, source: object):
        self.id = id
        self._parse_source(source)
        self._logger = logging.getLogger('field')

    def _parse_source(self, source):
        self.metadata = source['metadata']
        self.cropInfo = source['cropFenology']
        self.damages = source['damages'] if 'damages' in source else None
        self.treatments = source['treatments'] if 'treatments' in source else None
        self.irrigations = source['irrigation'] if 'irrigation' in source else None
        self.harvests = source['harvest'] if 'harvest' in source else None
        self.baling = source['baling'] if 'baling' in source else None
        self.heckling = source['heckling'] if 'heckling' in source else None
        self.bbch_stages = source['fenologies'] if 'fenologies' in source else None
        self.preparations = source['preparation'] if 'preparation' in source else None
        self.warnings = source['warnings'] if 'warnings' in source else None
        self.yields = source['yields'] if 'yields' in source else None
        self.application_maps = source['applicationmaps'] if 'applicationmaps' in source else None
        self.statistics = source['statistics'] if 'statistics' in source else None
        self.meteo = source['meteo'] if 'meteo' in source else None

    def to_json(self):
        field = dict()
        field['id'] = self.id
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
        field['meteo'] = self.meteo
        return field
