from pathlib import Path
import os

from generators import config_writer
from loaders import config_loader


def initializer() -> config_loader.LoadData:
    """Função para inicializar os parametros do sistema

    Inicializa os parametros do sistema, caso não exista o arquivo de configuração
    um novo arquivo é gerado

    :return: Instancia de configuração do sistema
    """
    file = Path('rpa_cotz.ini')
    if not file.exists():
        config_writer.create_config()

    return config_loader.LoadData()


if __name__ == '__main__':
    app_config = initializer()
    if app_config.is_valid:
        ...


