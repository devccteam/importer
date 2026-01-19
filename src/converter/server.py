import json
from http import HTTPStatus
from pathlib import Path
from typing import Annotated, Any

from fastapi import FastAPI, Form, HTTPException, Response, UploadFile

from converter.layouts.loader import (
    get_info_layout,
)
from converter.tasks.processa import processa_arquivo
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo, save_file
from converter.uteis.rest import (
    get_status,
    update_conversion,
)

app = FastAPI()

logger = config_logger.setup('app')


@app.get('/layout/{layout_id}')
async def layout(layout_id: str, response: Response) -> dict[str, Any]:
    try:
        info = get_info_layout(layout_id)

        if type(info) is not dict:
            response.status_code = HTTPStatus.NOT_FOUND

        return info
    except Exception as e:
        logger.exception(
            f'Erro no endpoint /layout: {e}',
            extra={'layout_id': layout_id},
            stack_info=True,
        )
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={
                'message': 'Ocorreu um erro interno. Tente novamente mais tarde.',
            },
        )


@app.post('/convert/layout/{layout_id}', status_code=HTTPStatus.CREATED)
async def converter(
    layout_id: int, file: UploadFile, password: Annotated[str, Form()] = ''
) -> dict[str, str]:
    id = ''
    try:

        suffix = Path(file.filename or "").suffix
        dir_file = await save_file(file, suffix)

        file_obj = Arquivo(file_dir=dir_file, password=password)

        id = processa_arquivo(str(layout_id), file_obj)

        return {'id': id, 'status': 'Running'}
    except Exception as e:
        logger.exception(
            f'Erro na no endpoint /converter: {e}',
            extra={'layout_id': layout_id, 'id': id},
            stack_info=True,
        )
        update_conversion(id, 'Error')
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={
                'status': 'FAILURE',
                'message': 'Ocorreu um erro interno. Tente novamente mais tarde.',
            },
        )


@app.get('/convert/{id}')
async def status(id: str) -> dict[str, Any]:
    try:
        data = get_status(id)

        return data

    except Exception as e:
        logger.exception(
            f'Erro na no endpoint /status: {e}',
            extra={'id': id},
            stack_info=True,
        )
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={
                'status': 'FAILURE',
                'message': 'Ocorreu um erro interno. Tente novamente mais tarde.',
            },
        )
