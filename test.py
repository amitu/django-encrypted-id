import os
from encrypted_id import encode, decode

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.tekey.settings'

# r = decode('w5HrsStQekdepSy8nCXXOg', 'statistic_public_access')

ekey = encode(812, 'user')

id = decode(ekey, 'user')

print(ekey, id)
