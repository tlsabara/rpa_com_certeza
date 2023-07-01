import json
from datetime import datetime
from jose import jwe

PUBLIC_KEY = b"""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCirMTyaFfydoUw8DfWQjw6xAYU
uoF/1VBJPrRke23kMS9pe47i8YPP8UW0HSECnUUXGbIkRSblpptFFHwpr0XuN/K3
xG67XR789aSNRsMx2amXQQ0jGapU8vUgmGEzh2udGzlsGdV5154fLHHe+D5sC1Rr
PQgo1hyolw2JqmuFgQIDAQAB
-----END PUBLIC KEY-----"""


params = dict(
    username='thiago.sabara@4mti.com.br',
    password='MinhaEmpresa',
    created_at=str(datetime.now()),
    csv_file='rpa_data.csv',
    chromedrive_file='chromedriver.exe'
)
jwt_config = jwe.encrypt(json.dumps(params), PUBLIC_KEY, algorithm='RSA1_5', encryption='A128GCM')

with open('../config_file.ini', 'w') as fl:
    fl.write(jwt_config.decode('utf-8'))
