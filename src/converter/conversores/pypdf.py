from pathlib import Path
from uuid import uuid4

from pypdf import PdfReader

DIR_TEMP = Path('temp')


def extract_text_from_pdf(file_path: Path, password: str = '') -> Path:
    file_out = DIR_TEMP / f'{uuid4()}.txt'

    try:
        DIR_TEMP.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            raise FileNotFoundError(f'Arquivo {file_path}, não encontrado')

        reader = PdfReader(file_path)

        if reader.is_encrypted and not password:
            raise Exception(
                'Necessário fornecer a senha para desbloquear o arquivo.'
            )

        if reader.is_encrypted:
            reader.decrypt(password)

        extracted_text: bytes

        with open(file_out, 'wb') as out:
            for page in reader.pages:
                extracted_text = page.extract_text(
                    extraction_mode='layout'
                ).encode('utf8')

                if extracted_text:
                    out.write(extracted_text)

        return file_out.resolve()
    except Exception as e:
        if file_out.exists():
            file_out.unlink()
        raise Exception(
            'Houve um erro na conversão do arquivo usando o PyPDF'
        ) from e
