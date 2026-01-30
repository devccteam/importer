import json
from http import HTTPStatus
from pathlib import Path
from typing import Annotated, Any

from fastapi import FastAPI, Form, Header, Request, Response, UploadFile
from fastapi.responses import JSONResponse

from converter.errors.error import BaseError
from converter.layouts.loader import (
    get_info_layout,
)
from converter.tasks.processa import processa_arquivo
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo, save_file, save_layout, valida_layout
from converter.uteis.rest import (
    get_status,
)

app = FastAPI()

logger = config_logger.setup('app')


@app.exception_handler(BaseError)
async def base_error_handler(_: Request, exc: BaseError) -> JSONResponse:
    logger.exception(f'Erro interno: {exc.detail}')

    return JSONResponse(status_code=exc.code, content={'message': exc.message})


@app.get('/layout/{layout_id}')
async def layout(layout_id: str, response: Response) -> dict[str, Any]:
    info = get_info_layout(layout_id)

    if type(info) is not dict:
        response.status_code = HTTPStatus.NOT_FOUND

    return info


@app.post('/layout/upload/{layout_id}', status_code=HTTPStatus.NO_CONTENT)
async def upload_layout(layout_id: int, file: UploadFile) -> None:
    await save_layout(str(layout_id), file.file)


@app.post('/layout/validate/{layout_id}', status_code=HTTPStatus.OK)
async def validate_layout(layout_id: int) -> None:
    await valida_layout(str(layout_id))


@app.post('/convert/layout/{layout_id}', status_code=HTTPStatus.CREATED)
async def converter(
    layout_id: int,
    file: UploadFile,
    password: Annotated[str, Form()] = '',
    input_val: Annotated[str, Form(alias='input')] = '',
    x_sandbox: Annotated[bool, Header(alias='X-Sandbox')] = False,
) -> dict[str, str]:
    id_task = ''
    input_json = {'': ''}

    layout: str = str(layout_id)

    suffix = Path(file.filename or '').suffix
    dir_file = await save_file(file.file, suffix)

    if input_val:
        try:
            input_json = json.loads(input_val)
        except json.JSONDecodeError:
            return {'erro': 'JSON inválido'}

    file_obj = Arquivo(file_dir=dir_file, password=password, input_val=input_json)

    if x_sandbox:
        layout = f'{layout}_sandbox'

    id_task = processa_arquivo(layout, file_obj)

    return {'id': id_task, 'status': 'Running'}


@app.get('/convert/{id_task}')
async def status(id_task: str) -> dict[str, Any]:
    return get_status(id_task)
