from decimal import Decimal
from pathlib import Path
from charset_normalizer import from_path

import pandas as pd

from converter.layouts.lancamento import Lancamento
from converter.layouts.layout_base import LayoutBase
from converter.layouts.layout_info import LayoutInfo
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo, get_encoding

logger = config_logger.setup('app.layouts')

FILE = Path(__file__).stem

class Processador(LayoutBase):
    layout = LayoutInfo('SOFTWARE', 'GENESIS', 'RELATÓRIO DE MOVIMENTAÇÕES FINANCEIRAS')

    def processar(self, id_task: str, file_obj: Arquivo) -> None:
        try:
            lancamento = Lancamento(id_task=id_task)
            coluns = ['Descrição', 'Data', 'Valor']
            dtype_config = {'Valor': str}
            encoding = get_encoding(file_obj.file_dir)

            for chunk in pd.read_csv(
                file_obj.file_dir,
                chunksize=100,
                sep=';',
                usecols=coluns,
                parse_dates=['Data'],
                date_format='%d/%m/%Y %H:%M:%S',
                encoding=encoding,
                dtype=dtype_config,
            ):
                for _, row in chunk.iterrows():
                    lancamento.Novo()
                    lancamento.hist = row['Descrição']
                    lancamento.data = row['Data']
                    lancamento.valor = Decimal(row['Valor'])
                    lancamento.cd = 'C' if lancamento.valor > 0 else 'D'
                    lancamento.incluir()

            lancamento.salvar()

        except Exception as e:
            logger.exception(f'Erro no layout {FILE}: {e}', extra={'id_task': id_task})
            raise Exception(f'Houve um erro no layout {FILE}') from e

        finally:
            if file_obj.file_dir and file_obj.file_dir.exists():
                file_obj.file_dir.unlink()
