import json
from datetime import datetime
from jose import jwe


# Realize o replace das keys do programa para melhorar a segurança

PUBLIC_KEY = b"""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCirMTyaFfydoUw8DfWQjw6xAYU
uoF/1VBJPrRke23kMS9pe47i8YPP8UW0HSECnUUXGbIkRSblpptFFHwpr0XuN/K3
xG67XR789aSNRsMx2amXQQ0jGapU8vUgmGEzh2udGzlsGdV5154fLHHe+D5sC1Rr
PQgo1hyolw2JqmuFgQIDAQAB
-----END PUBLIC KEY-----"""


def create_config() -> bool:
    try:
        username_ = input("\n\nInsira seu usuário do sistema:")
        password_ = input("\n\nInsira sua senha do sistema:")
        csv_ = input("\n\nInsira o caminho para o CSV com os dados:")

        params = dict(
            username=username_,
            password=password_,
            created_at=str(datetime.now()),
            csv_file=csv_,
        )

        jwt_config = jwe.encrypt(
            json.dumps(params), PUBLIC_KEY, algorithm="RSA1_5", encryption="A128GCM"
        )

        with open("rpa_cotz.ini", "w") as fl:
            fl.write(jwt_config.decode("utf-8"))

    except Exception as e:
        print(f'<<{"ERRO AO GERAR ARQUIVO":-^50}>>')
        print(e)
        print(f'<<{"FIM ERRO":-^50}>>')
        return False

    else:
        return True
