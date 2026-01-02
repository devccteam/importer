import importlib.util
import json
from pathlib import Path
from typing import Callable

from converter.uteis import config_logger
from converter.uteis.rest import check_dll

logger = config_logger.setup('app.layouts')

ProcessFunction = Callable[[str, int, Path], None]


def check_if_layout_file_exists(file: str) -> bool:
    exists: bool = False

    diretorio_atual = Path(__file__).parent
    caminho_arquivo = Path(
        diretorio_atual / f'{file}.py',
    )

    if caminho_arquivo.exists():
        exists = True

    return exists


def get_function_from_layout(file: str, func: str) -> Callable:
    try:
        # Tenta importar o módulo dinamicamente
        diretorio_atual = Path(__file__).parent
        caminho_arquivo = Path(
            diretorio_atual / f'{file}.py',
        )

        if not caminho_arquivo.exists():
            raise FileNotFoundError(
                f'Arquivo {caminho_arquivo} não encontrado'
            )

        spec = importlib.util.spec_from_file_location(file, caminho_arquivo)

        if not spec:
            raise Exception('Erro ao carregar o spec')

        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        return getattr(modulo, func)
    except Exception as e:
        logger.exception(f'Falha ao carregar {file}.py: {e}')
        raise Exception(f'Erro ao carregar {file}.py') from e


def obter_processador(nome_arquivo: str) -> ProcessFunction:
    try:
        return get_function_from_layout(nome_arquivo, 'processar')
    except Exception as e:
        raise e


def check_layout_info(layout_id: str) -> dict | str:
    try:
        info = get_function_from_layout(layout_id, 'info_layout')

        return info()
    except Exception as e:
        raise e


def get_info_layout(layout_id: str) -> dict | str:
    exist_file = check_if_layout_file_exists(layout_id)

    if exist_file:
        return check_layout_info(layout_id)

    data = check_dll(layout_id).data

    try:
        result = json.loads(data.decode('utf-8'))
    except json.JSONDecodeError:
        result = data.decode('utf-8')
    except UnicodeDecodeError as e:
        logger.exception(f'Erro ao converter a resposta da api para json: {e}')
        raise e

    return result
