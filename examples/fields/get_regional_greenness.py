import os
import datetime

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
#                  MAIN
# ---------------------------------------------------------
from pywig import Wig

wig = Wig()
wig.authenticate_basic(username=os.getenv('username'), password=os.getenv('password'))
fields = wig.get_fields()
field_id = fields[0].id
stats = wig.get_regional_greenness(field_id)

print(stats)
