import re
from decimal import Decimal


def RetornaTotalValoresValidos(linha: str) -> int:
    return len(re.findall(r'([0-9]\d{0,2}(?:\.\d{3})*,\d{2})', linha))


def RetornaValorFinalLinha(
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
