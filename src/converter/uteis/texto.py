import re
from re import Pattern
from typing import Final

REGEX_ULTIMA_COLUNA: Final[Pattern[str]] = re.compile(r'\s{2,}(\S.*)$')


def retorna_texto_final_linha_ate_espaco_duplo(
    linha: str, limpar_linha: bool = True
) -> tuple[str, str]:
    linha_tratada = linha.rstrip()
    if match := REGEX_ULTIMA_COLUNA.search(linha_tratada):
        resultado = match.group(1).strip()

        if limpar_linha:
            linha = linha[: match.start()].strip()

        return resultado, linha

    return '', linha
