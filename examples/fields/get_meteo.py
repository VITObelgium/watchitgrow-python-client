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
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 3, 1)
field_id = fields[0].id
stats = wig.get_meteo(field_id, key='temperature', start_date=start_date, end_date=end_date)

print(stats)
