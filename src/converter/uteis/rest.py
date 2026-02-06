import json
from http import HTTPStatus
from pathlib import Path
from typing import Any

import urllib3
from urllib3.exceptions import HTTPError

from converter.errors.error import APIError, error_decorator
from converter.settings import settings
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo

BASE_URL = settings.URL_API_PGRST
BASE_DLL_URL = settings.URL_API_DLL

http = urllib3.PoolManager()

logger = config_logger.setup('app.uteis')

type ResponseAPI = dict[str, Any]


def post(where: str, data: dict[str, Any]) -> ResponseAPI:
    try:
        encoded_data = json.dumps(data).encode('utf-8')

        response = http.request(
            'POST',
            BASE_URL + where,
            body=encoded_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )

        if response.status != HTTPStatus.CREATED:
            raise APIError(f'Erro na requisição: {response.json()}')

        if not response.data:
            return {}

        return response.json()

    except HTTPError as e:
        logger.exception(
            'Erro na requisição post',
            extra={'BASE_URL': BASE_URL, 'where': where},
            stack_info=True,
        )
        raise APIError('Erro na requisição post', detail=str(e)) from e
    except Exception as e:
        logger.exception(
            f'Erro na requisição post: {e}',
            extra={'BASE_URL': BASE_URL, 'where': where},
            stack_info=True,
        )
        raise Exception('Erro na requisição post') from e


def path(where: str, data: dict[Any, Any]) -> ResponseAPI:
    try:
        encoded_data = json.dumps(data).encode('utf-8')

        response = http.request(
            'PATCH',
            BASE_URL + where,
            body=encoded_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )

        if response.status != HTTPStatus.NO_CONTENT:
            raise APIError(f'Erro na requisição: {response.json()}')

        if not response.data:
            return {}

        return response.json()

    except HTTPError as e:
        logger.exception(
            'Erro na requisição path',
            extra={'BASE_URL': BASE_URL, 'where': where},
            stack_info=True,
        )
        raise APIError('Erro na requisição path') from e
    except Exception as e:
        logger.exception(
            'Erro na requisição path',
            extra={'BASE_URL': BASE_URL, 'where': where},
            stack_info=True,
        )
        raise Exception('Erro desconhecido ao fazer path') from e


def get_status(task_id: str) -> ResponseAPI:
    try:
        response = http.request(
            'GET',
            BASE_URL + f'/conversions?id=eq.{task_id}',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )

        data = response.json()

        if not data:
            return {}

        return data[0]

    except HTTPError as e:
        logger.exception(
            'Erro na requisição get',
            extra={
                'BASE_URL': BASE_URL,
                'where': f'/conversions?id=eq.{task_id}',
            },
            stack_info=True,
        )
        raise APIError('Erro na requisição path') from e
    except Exception as e:
        logger.exception(
            f'Erro na requisição get: {e}',
            extra={
                'BASE_URL': BASE_URL,
                'where': f'/conversions?id=eq.{task_id}',
            },
            stack_info=True,
        )
        raise Exception('Erro desconhecido ao verificar o status') from e


@error_decorator('Houve um erro ao inserir em releases')
def insert_releases(data: dict[str, Any]) -> ResponseAPI:
    return post('/releases', data)


@error_decorator('Houve um erro ao criar em conversion')
def create_conversion(id_task: str) -> ResponseAPI:
    data = {'id': id_task}

    return post('/conversions', data)


@error_decorator('Houve um erro ao atualizar o status em conversion')
def update_conversion(id_task: str, status: str) -> ResponseAPI:
    data = {'updated_at': 'now()', 'status': status}

    return path(f'/conversions?id=eq.{id_task}', data)


def check_dll(layout_id: str) -> ResponseAPI:
    try:
        response = http.request(
            'GET',
            BASE_DLL_URL + f'/layout/{layout_id}',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )

        return response.json()
    except HTTPError as e:
        logger.exception(
            f'Erro na requisição /layout: {e}',
            extra={'BASE_URL': BASE_DLL_URL, 'where': f'/layout/{layout_id}'},
            stack_info=True,
        )
        raise APIError('Erro ao checar a DLL na API', detail=str(e)) from e
    except Exception as e:
        logger.exception(
            f'Erro na requisição /layout: {e}',
            extra={'BASE_URL': BASE_DLL_URL, 'where': f'/layout/{layout_id}'},
            stack_info=True,
        )
        raise Exception('Erro não mapeado ao checar a DLL') from e


def process_dll(layout_id: str, file: Arquivo) -> ResponseAPI:
    try:
        with open(file.file_dir, 'rb') as f:
            content = f.read()

        form_data = {
            'file': (file.file_dir.name, content),
            'password': file.password,
            'input': json.dumps(file.input_val),
        }

        response = http.request(
            'POST',
            BASE_DLL_URL + f'/convert/layout/{layout_id}',
            fields=form_data,
        )

        return response.json()
    except HTTPError as e:
        logger.exception(
            f'Erro na requisição /convert/layout: {e}',
            extra={'BASE_URL': BASE_DLL_URL, 'where': f'/layout/{layout_id}'},
            stack_info=True,
        )
        raise APIError(
            'Erro ao enviar o arquivo para ser processado na DLL', detail=str(e)
        ) from e
    except Exception as e:
        logger.exception(
            f'Erro não mapeado na requisição /convert/layout: {e}',
            extra={'BASE_URL': BASE_DLL_URL, 'where': f'/layout/{layout_id}'},
            stack_info=True,
        )
        raise Exception(
            'Erro desconhecido ao enviar arquivo para processamento de DLL'
        ) from e
    finally:
        Path(file.file_dir).unlink()


def rest_done(filter_sql: str) -> None:
    where = f'/releases?{filter_sql}'
    try:
        response = http.request(
            'DELETE',
            BASE_URL + where,
        )

        logger.info(response.status)
        if response.status != HTTPStatus.NO_CONTENT:
            raise APIError(f'Erro na requisição: {response.json()}')

    except HTTPError as e:
        logger.exception(
            f'Erro ao apagar releases: {e}',
            extra={'BASE_URL': BASE_URL, 'where': where},
            stack_info=True,
        )
        raise APIError('Erro ao apagar releases', detail=str(e)) from e
    except Exception as e:
        logger.exception(
            f'Erro ao apagar releases: {e}',
            extra={'BASE_URL': BASE_URL, 'where': where},
            stack_info=True,
        )
        raise Exception('Erro ao apagar releases') from e
