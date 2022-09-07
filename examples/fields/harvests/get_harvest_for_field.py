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

field = wig.get_field_details(id=field_id)

print(json.dumps(field.harvests, indent=4))
