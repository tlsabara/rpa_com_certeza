from pathlib import Path
import os

from generators import config_writer
from loaders import config_loader
from rcc_pkg.rotines import RPARegister

__version__ = "0.0.0"


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
        rpa = RPARegister(app_config)
        rpa.register_today()
    # TODO: Completar os testes da rotina
    # TODO: Gerar o CSV de exemplo

