from pathlib import Path

from converter.conversores.pymupdf import extract_text_from_pdf
from converter.layouts.lancamento import Lancamento
from converter.layouts.layout_info import LayoutInfo
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo, ler_txt
from converter.uteis.datas import (
    RetornaDataInicioLinha,
    RetornaTotalDatasValidas,
)
from converter.uteis.texto import RetornaTextoFinalLinhaAteEspacoDuplo
from converter.uteis.valores import (
    RetornaTotalValoresValidos,
    RetornaValorFinalLinha,
)

logger = config_logger.setup('app.layouts')


def info_layout() -> dict:
    layout = LayoutInfo('SOFTWARE', 'GENESIS', 'RELATÓRIO DE MOVIMENTAÇÕES FINANCEIRAS')

    return layout.AsJson()


def processar(id_task: str, file_obj: Arquivo) -> None:
    path_dir: Path = Path('')

    try:
        lancamento = Lancamento(id_task=id_task)

        path_dir = extract_text_from_pdf(file_obj.file_dir, file_obj.password)

        pos_credito = 0

        # processa as linhas do arquivo
        for chunk in ler_txt(path_dir):
            data = chunk.splitlines()
            for index in range(len(data)):
                linha = data[index]

                if linha.startswith('Data'):
                    pos_credito = linha.find('Crédito')
                    continue

                if (
                    RetornaTotalDatasValidas(linha) >= 1
                    and RetornaTotalValoresValidos(linha) >= 2
                ):
                    lancamento.Novo()

                    if linha[pos_credito : pos_credito + 14].find(','):
                        lancamento.cd = 'C'
                    else:
                        lancamento.cd = 'D'

                    lancamento.data, linha = RetornaDataInicioLinha(linha)

                    _, linha = RetornaValorFinalLinha(linha)

                    lancamento.valor, linha = RetornaValorFinalLinha(linha)

                    lancamento.numdoc, linha = RetornaTextoFinalLinhaAteEspacoDuplo(
                        linha
                    )

                    lancamento.hist = linha.strip()

                    lancamento.incluir()

        lancamento.salvar()

    except Exception as e:
        logger.exception('Erro no layout 6174', stack_info=True)
        raise Exception('Houve um erro no layout 6174') from e

    finally:
        if path_dir and path_dir.exists():
            path_dir.unlink()

        if file_obj.file_dir and file_obj.file_dir.exists():
            file_obj.file_dir.unlink()
