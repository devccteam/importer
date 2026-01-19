import re
from decimal import Decimal
from typing import Final, Pattern

REGEX_VALORES_VALIDOS: Final[Pattern[str]] = re.compile(r'([0-9]\d{0,2}(?:\.\d{3})*,\d{2})')
def retorna_total_valores(linha: str) -> int:
    count: int = 0

    for _ in REGEX_VALORES_VALIDOS.finditer(linha):
        count += 1

    return count

def retorna_valor_final_linha(
    linha: str, limpar_linha: bool = True
) -> tuple[Decimal, str]:
    try:
        valor_str = ''
        valor = Decimal(0)

        linha = linha.strip()

        if ' ' in linha:
            valor_str = linha.rsplit(' ', 1)[1]
        else:
            valor_str = linha

        valor_str = valor_str.replace('R$', '').replace('$', '').strip()
        valor_str = valor_str.replace('.', '').replace(',', '.')

        valor = Decimal(valor_str)

        if limpar_linha:
            linha = linha.rsplit(' ', 1)[0]

        return valor, linha

    except Exception:
        return Decimal(0), linha
