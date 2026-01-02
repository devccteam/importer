import uuid
from pathlib import Path
from typing import Generator

from pydantic import BaseModel, field_serializer


async def save_file(bytes_file: bytes, ext_file: str = '.pdf') -> Path:
    temp_dir_path = Path('temp') / f'{uuid.uuid4()}{ext_file}'

    temp_dir_path.parent.mkdir(parents=True, exist_ok=True)

    with open(temp_dir_path, 'wb') as buffer:
        buffer.write(await bytes_file.read())

    return Path(temp_dir_path.resolve())


def ler_txt(file_path: Path, chunk_size_mb: int = 100) -> Generator[str]:
    chunk_size_bytes = chunk_size_mb * 1024 * 1024
    buffer = b''
    with open(file_path, 'rb') as file:
        while True:
            data = buffer + file.read(chunk_size_bytes)
            if not data:
                break

            pos_last_line = data.rfind(b'\n') + 1

            if pos_last_line != 0:
                buffer = data[pos_last_line:]
                data = data[:pos_last_line]
            else:
                buffer = b''

            yield data.decode('utf-8', errors='ignore')

        if buffer:
            yield buffer.decode('utf-8', errors='ignore')


class Arquivo(BaseModel):
    file_dir: Path
    password: str

    @field_serializer('file_dir')
    def serialize_file_dir(file_dir: Path) -> str:
        return str(file_dir)
