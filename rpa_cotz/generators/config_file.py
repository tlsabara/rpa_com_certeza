import json
from datetime import datetime

from jose import jwe

private = b"""-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCirMTyaFfydoUw8DfWQjw6xAYUuoF/1VBJPrRke23kMS9pe47i
8YPP8UW0HSECnUUXGbIkRSblpptFFHwpr0XuN/K3xG67XR789aSNRsMx2amXQQ0j
GapU8vUgmGEzh2udGzlsGdV5154fLHHe+D5sC1RrPQgo1hyolw2JqmuFgQIDAQAB
AoGAAyPUlV1APVTeU0h/u2oB4ZyBBYtoDoCekRtdvgbH4zyzzpRs+KJyyeO9VbGu
Pm+ssrpzPtH64znpC1dO4jsY3W1YwYFYB7cbKSGQHDFaXj+nQDeOPfId1gwMXNT+
dAZ0ljYwgWGSaY4TueDbTUjPww7ktObVLkIeFMuCN8JowsUCQQDjC9mLaNejDzdC
Fd8/8UGU1jxf0JUHRvEqy8Z5EPhUxHogB5sprMTXOfQmcDDW+K2JI0uwE92hLDdn
4v7RoZLfAkEAt2tzjYGGz4nBGlAySK3/PXBr6w9TG/GftQ5CK5mwL+XwbwIktEyA
STAq59EVHTczJPI6J4ypP8xwDZHmZO1TnwJAQhxyNPjLSWylz3Vk806BpSAYpmGq
81qB4M9DNH9vf+dSFD+Cu8jV7EGwyPyEDCSPC06evF+celDQtUxQnKPqiwJARPuc
kfPNB/D/Ny5COyN1g13suJMi5reRIT8jk9JReTI5owZjV4wOE3iSKm1wS3SfP536
UTWN0fjJi9D7nanEcQJBAMTreIIPCQ70e9X4uah46WussvdKa/Y6r1ooJEN5rBEH
5u8UnoR3NV0hzFUVRWAX8S4uX2vSzmOUT+wISYKonC4=
-----END RSA PRIVATE KEY-----"""

public = b"""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCirMTyaFfydoUw8DfWQjw6xAYU
uoF/1VBJPrRke23kMS9pe47i8YPP8UW0HSECnUUXGbIkRSblpptFFHwpr0XuN/K3
xG67XR789aSNRsMx2amXQQ0jGapU8vUgmGEzh2udGzlsGdV5154fLHHe+D5sC1Rr
PQgo1hyolw2JqmuFgQIDAQAB
-----END PUBLIC KEY-----"""


params = dict(
    username='thiago.sabara@4mti.com.br',
    company='MinhaEmpresa',
    created_at=str(datetime.now()),
    valid_true=str(datetime(2023, 7, 5, 23, 59, 59))
)
jwt_config = jwe.encrypt(json.dumps(params), public,  algorithm='RSA1_5', encryption='A128GCM')

reversed_ = jwe.decrypt(jwt_config, private)
reversed_ = json.loads(reversed_)
with open('config_file.ini', 'w') as fl:
    fl.write(jwt_config.decode('utf-8'))
    fl.write('\n\n--------\n\n')
    # fl.write(reversed_.decode('utf-8'))
    fl.write(str(reversed_))
print('end')
