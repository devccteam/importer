from decimal import Decimal

import pandas as pd

from converter.layouts.lancamento import Lancamento
from converter.layouts.layout_info import LayoutInfo
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo

logger = config_logger.setup('app.layouts')


def info_layout() -> dict:
    layout = LayoutInfo('SOFTWARE', 'GENESIS', 'RELATÓRIO DE MOVIMENTAÇÕES FINANCEIRAS')

    return layout.AsJson()


def processar(id_task: str, file_obj: Arquivo) -> None:
    try:
        lancamento = Lancamento(id_task=id_task)
        coluns = ['Descrição', 'Data', 'Valor']
        dtype_config = {'Valor': str}
        for chunk in pd.read_csv(
            file_obj.file_dir,
            chunksize=100,
            sep=';',
            usecols=coluns,
            parse_dates=['Data'],
            encoding='utf-8',
            dtype=dtype_config,
        ):
            for _, row in chunk.iterrows():
                lancamento.Novo()
                lancamento.hist = row['Descrição']
                lancamento.data = row['Data']
                lancamento.valor = Decimal(row['Valor'])
                lancamento.cd = 'C' if lancamento.valor > 0 else 'D'
                lancamento.incluir()

    except Exception as e:
        logger.exception('Erro no layout 6174')
        raise Exception('Houve um erro no layout 6174') from e

    finally:
        if file_obj.file_dir and file_obj.file_dir.exists():
            file_obj.file_dir.unlink()
