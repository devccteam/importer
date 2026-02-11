import json
from http import HTTPStatus
from pathlib import Path
from typing import Annotated, Any
from urllib.parse import unquote

from fastapi import FastAPI, Form, Header, Request, Response, UploadFile
from fastapi.responses import JSONResponse

from converter.errors.error import BaseError
from converter.layouts.loader import (
    get_info_layout,
)
from converter.models.new_layout import NewLayout
from converter.tasks.processa import processa_arquivo
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo, save_file, save_layout, valida_layout
from converter.uteis.rest import (
    get_layouts,
    get_status,
    post_create_layout,
    rest_done,
)

app = FastAPI()

logger = config_logger.setup('app')


@app.exception_handler(BaseError)
async def base_error_handler(_: Request, exc: BaseError) -> JSONResponse:
    logger.exception(f'Erro interno: {exc.detail}')

    return JSONResponse(status_code=exc.code, content={'message': exc.message})


@app.get(
    '/layouts',
    summary='Lista todos os layouts',
    description='Consulta pode ser feita usando os filtros do PostgREST',
    tags=['Layout - Consulta'],
)
async def list_layout(req: Request) -> list[dict[str, Any]] | list[str]:
    query = unquote(str(req.query_params))
    return get_layouts(query)


@app.get(
    '/layout/{layout_id}',
    summary='Verifica informações do layout',
    tags=['Layout - Consulta'],
)
async def layout(layout_id: str, response: Response) -> dict[str, Any]:
    info = get_info_layout(layout_id)

    if type(info) is not dict:
        response.status_code = HTTPStatus.NOT_FOUND

    return info


@app.post(
    '/layout/upload/{layout_id}',
    summary='Envia layout python',
    tags=['Layout - Gerenciamento'],
    status_code=HTTPStatus.NO_CONTENT,
)
async def upload_layout(layout_id: int, file: UploadFile) -> None:
    await save_layout(str(layout_id), file.file)


@app.post(
    '/layout/validate/{layout_id}',
    summary='Valida layout python',
    tags=['Layout - Gerenciamento'],
    status_code=HTTPStatus.OK,
)
async def validate_layout(layout_id: int) -> None:
    await valida_layout(str(layout_id))


@app.post(
    '/layout/create',
    summary='Cria novo layout',
    tags=['Layout - Gerenciamento'],
    status_code=HTTPStatus.CREATED,
)
async def create_layout(info_layout: NewLayout) -> dict[str, int]:
    return post_create_layout(info_layout)


@app.post(
    '/convert/layout/{layout_id}',
    summary='Converter arquivo',
    tags=['Convert'],
    status_code=HTTPStatus.CREATED,
)
async def converter(
    layout_id: int,
    file: UploadFile,
    password: Annotated[str, Form()] = '',
    input_val: Annotated[str, Form(alias='input')] = '',
    x_sandbox: Annotated[bool, Header(alias='X-Sandbox')] = False,
) -> dict[str, str]:
    """Inica conversão do arquivo enviado, com base no codigo"""
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


@app.get('/convert/{id_task}', tags=['Convert'], summary='Checa status da conversão')
async def status(id_task: str) -> dict[str, Any]:
    """Checa o status da conversão de um arquivo"""
    return get_status(id_task)


@app.post(
    '/convert/{id_task}/done',
    tags=['Convert'],
    summary='Limpa conversão',
    status_code=HTTPStatus.NO_CONTENT,
)
async def done(id_task: str) -> None:
    """Limpa a importação da API"""
    rest_done(f'conversions_id=eq.{id_task}')
