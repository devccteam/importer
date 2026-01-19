import re
from datetime import date, datetime
from typing import Final, Pattern


def DataPadrao() -> date:
    return date(1934, 12, 12)

REGEX_DATAS_VALIDAS: Final[Pattern[str]] = re.compile(r'\b\d{2}/\d{2}/(?:\d{4}|\d{2})\b')
def retorna_total_datas(linha: str) -> int:
    count: int = 0
    for _ in REGEX_DATAS_VALIDAS.finditer(linha):
        count += 1

    return count


REGEX_DATA_INICIO: Final[Pattern[str]] = re.compile(r'^\d{2}\/\d{2}\/(\d{4}|\d{2})')
def retorna_data_inicio_linha(
    linha: str, limpar_linha: bool = True
) -> tuple[date, str]:
    try:

        if not (match := REGEX_DATA_INICIO.match(linha)):
            return DataPadrao(), linha

        data_str = match.group(linha)

        fmt = '%d/%m/%Y' if len(data_str) == 10 else '%d/%m/%y'
        data = datetime.strptime(data_str, fmt).date()

        if limpar_linha:
            linha = linha[match.end():].lstrip()

        return data, linha
    except Exception:
        return DataPadrao(), linha
