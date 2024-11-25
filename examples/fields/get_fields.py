

# ---------------------------------------------------------
#                  MAIN
# ---------------------------------------------------------
from ./pywig import Wig

wig = Wig()
wig.authenticate_basic(username='demo@vito.be', password='demo123456')
print(wig._auth.get_token())

fields = wig.get_fields()

print(fields)
