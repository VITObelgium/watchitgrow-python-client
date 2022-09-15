import os
import datetime

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
#                  MAIN
# ---------------------------------------------------------
from pywig import Wig

field_id = '<FIELD_ID>'

wig = Wig()
wig.authenticate_basic(username=os.getenv('username'), password=os.getenv('password'))

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 3, 1)
stats = wig.get_meteo(field_id, key='temperature', start_date=start_date, end_date=end_date)

print(stats)
