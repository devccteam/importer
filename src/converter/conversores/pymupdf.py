from pathlib import Path
from time import time
from uuid import uuid4

import pymupdf

from converter.uteis import config_logger

logger = config_logger.setup('app.conversor')


DIR_TEMP = Path('temp')


def extract_text_from_pdf(file_path: Path, password: str = '') -> Path:
    file_out = DIR_TEMP / f'{uuid4()}.txt'

    try:
        DIR_TEMP.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            logger.exception(
                f'Arquivo não encontrado: {file_path}', stack_info=True
            )
            raise FileNotFoundError(f'Arquivo {file_path}, não encontrado')

        with pymupdf.open(file_path) as doc:
            start_conversion = time()
            logger.info(
                f'Iniciando conversão do {file_path.name}',
                extra={'Total de paginas': doc.page_count},
            )

            if doc.is_encrypted and not password:
                logger.exception(
                    f'Arquivo tem senha, e não foi fornecida: {file_path}'
                )
                raise Exception(
                    'Necessário fornecer a senha para desbloquear o arquivo.'
                )

            if doc.is_encrypted:
                doc.authenticate(password)

            extracted_text: bytes

            with open(file_out, 'wb') as out:
                for index, page in enumerate(doc):
                    extracted_text = page.get_text(sort=True).encode('utf8')
                    if extracted_text:
                        out.write(extracted_text)

        end_conversion = time()

        logger.info(
            f'Finalizou a conversão do arquivo: {file_path.name}',
            extra={'Tempo total': f'{end_conversion - start_conversion:.2f}s'},
        )

        return file_out.resolve()
    except Exception as e:
        logger.exception(
            'Houve um erro na conversão do arquivo usando o PyMuPdf',
            stack_info=True,
        )
        if file_out.exists():
            file_out.unlink()
        raise Exception(
            'Houve um erro na conversão do arquivo usando o PyMuPdf'
        ) from e
