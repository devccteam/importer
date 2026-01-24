import re
from decimal import Decimal
from re import Pattern
from typing import Final

REGEX_VALORES_VALIDOS: Final[Pattern[str]] = re.compile(
    r'([0-9]\d{0,2}(?:\.\d{3})*,\d{2})'
)


def retorna_total_valores(linha: str) -> int:
    count: int = 0

    for _ in REGEX_VALORES_VALIDOS.finditer(linha):
        count += 1

    return count


REGEX_VALOR_FINAL_LINHA: Final[Pattern[str]] = re.compile(
    r'(?:R\$\s*)?(\d{1,3}(\.\d{3})*\,\d{2})$'
)


def retorna_valor_final_linha(
    linha: str, limpar_linha: bool = True
) -> tuple[Decimal, str]:
    linha = linha.strip()
    if match := REGEX_VALOR_FINAL_LINHA.search(linha):
        valor_bruto = match.group()
        try:
            valor_limpo = valor_bruto.replace('.', '').replace(',', '.')
            valor = Decimal(valor_limpo)

            if limpar_linha:
                linha = linha[: match.start()].strip()

            return valor, linha
        except Exception:
            pass

    return Decimal(0), linha
