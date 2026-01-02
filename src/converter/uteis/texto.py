def RetornaTextoFinalLinhaAteEspacoDuplo(
    linha: str, limpar_linha: bool = True
) -> tuple[str, str]:
    resultado: str = ''
    temp: str = linha.strip()

    if '  ' in temp:
        resultado = temp.rsplit('  ', 1)[1]
    else:
        resultado = ''

    if limpar_linha:
        temp = temp.rsplit('  ', 1)[0]

    return resultado, temp
