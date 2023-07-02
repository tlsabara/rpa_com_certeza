import json
from datetime import datetime
from jose import jwe
import pandas as pd

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


class LoadData:
    """Classe para tratamento do arquivo de configuração com os dados do usuário

    Esta classe serve como um wrapper para os dados de usuário e senha e valores dos dias a serem inseridos
    """

    def __init__(self) -> None:
        self.__valid = False
        self.__trace_error = None
        data = self.__load_data()

        self.username: str = data.get("username")
        self.password: str = data.get("password")
        self.create_at: str = data.get("create_at")
        self.csv_file: str = data.get("csv_file")
        self.df_data: pd.DataFrame = data.get("df_data")

    @property
    def is_valid(self) -> bool:
        """Retorno simples sobre a validade da configuração

        :return: Boleando informando se a configuração é válida ou não
        """
        return self.__valid

    @property
    def error_trace(self) -> str:
        """Interface de retorno do erro da configuração

        :return:
        """
        return self.__trace_error

    def __load_data(self) -> dict:
        """Carrega o arquivo de configuração para um dicionário

        :return: dicionário com os dados de configuração
        """
        try:
            with open("rpa_cotz.ini", "r") as fl:
                jwt_config = fl.readline()
            reversed_ = jwe.decrypt(jwt_config, PRIVATE_KEY)
            reversed_ = json.loads(reversed_)
            reversed_["df_data"] = self.__load_df_data(reversed_.get("csv_file"))
        except Exception as e:
            self.__trace_error = str(e)
            raise e
            # TODO: Melhorar este tratamento de erro, codificação do arquivo esta afetando o funcionanento
            # return dict()
        else:
            self.__valid = True
            return reversed_

    @staticmethod
    def __load_df_data(filename: str) -> pd.DataFrame:
        """Carregao arquivo apenas com os dados que devem ser trataos

        :param filename: caminho ou nome do arquivo
        :return: DataFrame com os dados a serem inseridos.
        """
        df = pd.read_csv(filename, sep=";")
        return df.query("INSERIDO == False and IGNORAR == False")

    def save_df_data(self) -> bool:
        """Interface para salvamento do arquivo CSV

        :return: Verdadeiro ou Falso para o salvamento do arquivo
        """
        try:
            self.df_data.to_csv(self.csv_file, sep=";", index=False, encoding="utf-8")
        except Exception as e:
            return False
        else:
            return True

    def next_record(self) -> pd.Series:
        """Interface para coleta de registros com os parametros necessários.

        :return:
        """
        for _, line in self.df_data.iterrows():
            yield line
