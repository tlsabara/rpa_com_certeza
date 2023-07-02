import pandas as pd


def generate(filename: str='example_file.csv') -> None:
    """Apenas cria um CSV de exemplo vazio"""
    columns_names = [
        'DATA',
        'TEXTO_ATIVIDADE',
        'HORAS_EMPRESA',
        'HORAS_CLIENTE',
        'HORAS_HOMEOFFICE',
        'EVENTO',
        'PESSOA',
        'PROJETO',
        'INSERIDO',
        'EXECUTION_STATUS',
        'IGNORAR',
    ]
    # Usamos sempre o sep como ";"
    pd.DataFrame(columns=columns_names).to_csv(filename, sep=';')
