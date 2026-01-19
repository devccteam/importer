import uuid
import shutil

from anyio import to_thread
from pathlib import Path

from charset_normalizer import from_path
from fastapi import UploadFile
from pydantic import BaseModel, FilePath

BUFFER_SIZE: int =  128 * 1024
async def save_file(upload_file: UploadFile, ext_file: str = '.pdf') -> Path:
    temp_dir_path = Path('temp') / f'{uuid.uuid4()}{ext_file}'

    temp_dir_path.parent.mkdir(parents=True, exist_ok=True)

    def _save_copy() -> None:
        with temp_dir_path.open('wb') as buffer:
            shutil.copyfileobj(upload_file.file, buffer, length=BUFFER_SIZE)

    await to_thread.run_sync(_save_copy)

    return temp_dir_path.resolve()


class Arquivo(BaseModel):
    file_dir: FilePath
    password: str

def get_encoding(file_dir: Path, default: str = 'utf-8') -> str:
    try:
        result = from_path(file_dir).best()

        if not result or not result.encoding:
            return default

        return str(result.encoding)

    except Exception:
        return default
