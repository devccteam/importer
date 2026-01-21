from collections.abc import Iterator
from pathlib import Path

from converter.conversores.pymupdf import extract_text_from_pdf
from converter.layouts.lancamento import Lancamento
from converter.layouts.layout_base import LayoutBase
from converter.layouts.layout_info import LayoutInfo
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo
from converter.uteis.datas import (
    retorna_data_inicio_linha,
    retorna_total_datas,
)
from converter.uteis.texto import retorna_texto_final_linha_ate_espaco_duplo
from converter.uteis.valores import (
    retorna_total_valores,
    retorna_valor_final_linha,
)

logger = config_logger.setup('app.layouts')

FILE = Path(__file__).stem


class Processador(LayoutBase):
    layout = LayoutInfo('SOFTWARE', 'GENESIS', 'RELATÓRIO DE MOVIMENTAÇÕES FINANCEIRAS')

    def processar(self, id_task: str, file_obj: Arquivo) -> None:
        path_dir: Path = Path('')

        try:
            lancamento = Lancamento(id_task=id_task)

            path_dir = extract_text_from_pdf(file_obj.file_dir, file_obj.password)

            pos_credito = 0

            # processa as linhas do arquivo
            with path_dir.open(mode='r', encoding='utf-8') as file:
                it: Iterator[tuple[int, str]] = enumerate(file)

                for _, linha in it:
                    if linha.startswith('Data'):
                        pos_credito = linha.find('Crédito')
                        continue

                    if (
                        retorna_total_datas(linha) >= 1
                        and retorna_total_valores(linha) >= 2
                    ):
                        lancamento.Novo()

                        if linha[pos_credito : pos_credito + 14].find(','):
                            lancamento.cd = 'C'
                        else:
                            lancamento.cd = 'D'

                        lancamento.data, linha = retorna_data_inicio_linha(linha)

                        _, linha = retorna_valor_final_linha(linha)

                        lancamento.valor, linha = retorna_valor_final_linha(linha)

                        lancamento.numdoc, linha = (
                            retorna_texto_final_linha_ate_espaco_duplo(linha)
                        )

                        lancamento.hist = linha.strip()

                        lancamento.incluir()

            lancamento.salvar()

        except Exception as e:
            logger.exception(f'Erro no layout {FILE}: {e}', extra={'id_task': id_task})
            raise Exception(f'Houve um erro no layout {FILE}') from e

        finally:
            if path_dir and path_dir.exists():
                path_dir.unlink()

            if file_obj.file_dir and file_obj.file_dir.exists():
                file_obj.file_dir.unlink()
