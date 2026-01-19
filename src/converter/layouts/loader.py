import importlib.util
import json
from pathlib import Path

from converter.layouts.layout_base import LayoutBase
from converter.uteis import config_logger
from converter.uteis.rest import check_dll

logger = config_logger.setup('app.layouts')


def check_if_layout_file_exists(file: str) -> bool:
    exists: bool = False

    diretorio_atual = Path(__file__).parent
    caminho_arquivo = Path(
        diretorio_atual / f'{file}.py',
    )

    if caminho_arquivo.exists():
        exists = True

    return exists


def get_instance_layout(file: str) -> LayoutBase:
    try:
        diretorio_atual = Path(__file__).parent
        caminho_arquivo = Path(
            diretorio_atual / f'{file}.py',
        )

        if not caminho_arquivo.exists():
            raise FileNotFoundError(f'Arquivo {caminho_arquivo} não encontrado')

        spec = importlib.util.spec_from_file_location(file, caminho_arquivo)

        if not spec:
            raise ImportError(f'{file} não foi encontrado')

        if spec.loader is None:
            raise ImportError('{file} não possui um loader válidoe')

        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        classe = getattr(modulo, 'Processador')

        if not issubclass(classe, LayoutBase):
            raise ImportError(f'{file}, não tem uma classe de layout valido')

        return classe()
    except Exception as e:
        logger.exception(f'Falha ao carregar {file}.py: {e}')
        raise Exception(f'Erro ao carregar {file}.py') from e


def check_layout_info(layout_id: str) -> dict[str, str]:
    try:
        layout = get_instance_layout(layout_id)

        return layout.info_layout()
    except Exception as e:
        raise e


def get_info_layout(layout_id: str) -> dict[str, str]:
    exist_file = check_if_layout_file_exists(layout_id)

    if exist_file:
        return check_layout_info(layout_id)

    data = check_dll(layout_id)

    return data
