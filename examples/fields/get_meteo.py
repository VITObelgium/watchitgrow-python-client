import json
import os

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
#                  MAIN
# ---------------------------------------------------------
from pywig import Wig

field_id = '<FIELD_ID>'

wig = Wig()
wig.authenticate_basic(username=os.getenv('username'), password=os.getenv('password'))

stats = wig.get_meteo(field_id, key='temperature')

print(stats)
