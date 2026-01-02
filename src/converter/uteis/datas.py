import re
from datetime import date, datetime


def DataPadrao() -> date:
    return date(1934, 12, 12)


def RetornaTotalDatasValidas(linha: str) -> int:
    return len(re.findall(r'([0-9]{2}\/[0-9]{2}\/[0-9]{2,4})', linha))


def RetornaDataInicioLinha(
    linha: str, limpar_linha: bool = True
) -> tuple[date, str]:
    try:
        regex_data_no_inicio = re.compile(r'^\d{2}\/\d{2}\/(\d{4}|\d{2})')

        if not regex_data_no_inicio.search(linha):
            return None

        data_str = regex_data_no_inicio.search(linha).group()

        data = datetime.strptime(data_str, '%d/%m/%Y').date()

        if limpar_linha:
            linha = linha.replace(data_str, '', 1)

        return data, linha
    except Exception:
        return DataPadrao(), linha
