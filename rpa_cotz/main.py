from pathlib import Path
import os

from generators import config_writer
from loaders import config_loader
from rcc_pkg.rotines import RPARegister

__version__ = "0.0.0"
CONFIG_FILENAME = "rpa_cotz.ini"


def initializer() -> config_loader.LoadData:
    """Função para inicializar os parametros do sistema

    Inicializa os parametros do sistema, caso não exista o arquivo de configuração
    um novo arquivo é gerado

    :return: Instancia de configuração do sistema
    """
    file = Path(CONFIG_FILENAME)
    if not file.exists():
        config_writer.create_config()

    return config_loader.LoadData()


def exec_app(config_instance: config_loader.LoadData, sub_routine=False) -> None:
    """Método de execução do programa

    Controla o fluxo de configuração, iniciando somente se a configuração for válida.
    """

    if config_instance.is_valid:
        rpa = RPARegister(config_instance)
        rpa.register_batch()
    else:
        print(config_instance.error_trace)
        file = Path(CONFIG_FILENAME)
        if not sub_routine and file.exists():
            file.unlink()
            exec_app(config_instance, sub_routine=True)


if __name__ == "__main__":
    app_config = initializer()
    exec_app(app_config)
    # TODO: Completar os testes da rotina
    # TODO: Gerar o CSV de exemplo
