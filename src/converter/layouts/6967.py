from collections.abc import Iterator
from pathlib import Path

from converter.layouts.lancamento import Lancamento
from converter.layouts.layout_base import LayoutBase
from converter.layouts.layout_info import LayoutInfo
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo
from converter.uteis.datas import retorna_data_inicio_linha, retorna_total_datas
from converter.uteis.texto import retorna_texto_final_linha_ate_espaco_duplo
from converter.uteis.valores import retorna_total_valores, retorna_valor_final_linha

logger = config_logger.setup('app.layouts')
FILE = Path(__file__).stem


class Processador(LayoutBase):
    layout = LayoutInfo('SOFTWARE', 'CUB', 'TOTAL CONTAS A PAGAR')

    def processar(self, id_task: str, file_obj: Arquivo) -> None:
        path_dir: Path = Path('')

        try:
            lancamento = Lancamento(id_task=id_task)
            path_dir = file_obj.file_dir

            # processa as linhas do arquivo
            with path_dir.open(mode='r', encoding='utf-8') as file:
                it: Iterator[tuple[int, str]] = enumerate(file)

                for _, linha in it:
                    if (
                        retorna_total_datas(linha) >= 1
                        and retorna_total_valores(linha) >= 2
                    ):
                        lancamento.Novo()
                        lancamento.cd = 'D'

                        linha = linha.replace('(', '')
                        linha = linha.replace(')', '')

                        lancamento.data, linha = retorna_data_inicio_linha(linha)
                        _, linha = retorna_valor_final_linha(linha)
                        lancamento.valor, linha = retorna_valor_final_linha(linha)
                        _, linha = retorna_texto_final_linha_ate_espaco_duplo(linha)
                        lancamento.hist, linha = (
                            retorna_texto_final_linha_ate_espaco_duplo(linha)
                        )

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
