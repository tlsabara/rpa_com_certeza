import json
from datetime import datetime
from jose import jwe

PRIVATE_KEY = b"""-----BEGIN RSA PRIVATE KEY-----
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

with open('config_file.ini', 'w') as fl:
    jwt_config = fl.readline()

reversed_ = jwe.decrypt(jwt_config, PRIVATE_KEY)
reversed_ = json.loads(reversed_)