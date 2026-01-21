import os
import uuid
from pathlib import Path
from typing import BinaryIO

import anyio
from anyio import to_thread
from charset_normalizer import from_path
from pydantic import BaseModel, FilePath

from converter.errors.error import FileError, async_error_decorator
from converter.uteis import config_logger

logger = config_logger.setup('app')


async def copy_file_to_disk(
    stream: BinaryIO,
    *,
    destination_directory: Path,
    filename: str,
    buffer_size: int = 128 * 1024,
) -> Path:
    base_dir = Path(destination_directory).resolve()
    safe_filename = Path(filename).name
    final_path = (base_dir / safe_filename).resolve()

    await to_thread.run_sync(base_dir.mkdir, 755, True, True)

    if final_path.exists():
        raise FileExistsError(f'O arquivo {final_path} já existe.')

    async with await anyio.open_file(final_path, 'wb') as buffer:
        while True:
            chunk = await to_thread.run_sync(stream.read, buffer_size)
            if not chunk:
                break
            await buffer.write(chunk)

    return final_path


@async_error_decorator('Erro ao salvar o arquivo enviado')
async def save_file(file: BinaryIO, suffix: str) -> Path:
    dest_path = Path('temp')
    name_file = f'{uuid.uuid4()}.{suffix}'
    saved_file = await copy_file_to_disk(
        file, destination_directory=dest_path, filename=name_file
    )

    return saved_file


@async_error_decorator('Erro ao salvar o layout')
async def save_layout(layout_id: str, file: BinaryIO) -> None:
    dest_path = Path('src/converter/layouts')
    name_file = f'{layout_id}_sandbox.py'
    await copy_file_to_disk(file, destination_directory=dest_path, filename=name_file)


@async_error_decorator('Error ao validar o layout')
async def valida_layout(layout_id: str) -> None:
    layout_dir = Path('src/converter/layouts')
    actual_layout = layout_dir / f'{layout_id}.py'
    sandbox_layout = layout_dir / f'{layout_id}_sandbox.py'
    old_layout = layout_dir / f'{layout_id}_old.py'

    if not sandbox_layout.exists():
        raise FileError(
            message='Layout sandbox não encontrado',
            detail=f'{sandbox_layout} não encontrado',
        )

    if actual_layout.exists():
        await to_thread.run_sync(os.replace, actual_layout, old_layout)

    await to_thread.run_sync(sandbox_layout.rename, actual_layout)


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
