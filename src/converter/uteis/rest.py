import json
from http import HTTPStatus

import urllib3
from urllib3.response import HTTPResponse

from converter.errors.error import error_decorator
from converter.settings import settings
from converter.uteis import config_logger

BASE_URL = settings.URL_API_PGRST
BASE_DLL_URL = settings.URL_API_DLL

http = urllib3.PoolManager()

logger = config_logger.setup('app.uteis')


def post(where: str, data: any) -> HTTPResponse:
    try:
        response = http.request(
            'POST',
            BASE_URL + where,
            body=json.dumps(data),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )

        if response.status != HTTPStatus.CREATED:
            raise Exception(f'Erro na requisição: {response.json()}')

        return response
    except Exception as e:
        logger.exception(
            f'Erro na requisição post: {e}',
            extra={'BASE_URL': BASE_URL, 'where': where},
            stack_info=True,
        )
        raise Exception('Erro na requisição post') from e


def path(where: str, data: dict[any, any]) -> HTTPResponse:
    try:
        response = http.request(
            'PATCH',
            BASE_URL + where,
            body=json.dumps(data),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )

        if response.status != HTTPStatus.NO_CONTENT:
            raise Exception(f'Erro na requisição: {response.json()}')

        return response

    except Exception as e:
        logger.exception(
            f'Erro na requisição path: {e}',
            extra={'BASE_URL': BASE_URL, 'where': where},
            stack_info=True,
        )
        raise Exception('Erro na requisição path') from e


def get_status(task_id: str) -> HTTPResponse:
    try:
        response = http.request(
            'GET',
            BASE_URL + f'/conversions?id=eq.{task_id}',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )

        return response
    except Exception as e:
        logger.exception(
            f'Erro na requisição get: {e}',
            extra={
                'BASE_URL': BASE_URL,
                'where': f'/conversions?id=eq.{task_id}',
            },
            stack_info=True,
        )
        raise Exception('Erro na requisição path') from e


@error_decorator('Houve um erro ao inserir em releases')
def insert_releases(data: dict) -> HTTPResponse:
    response = post('/releases', data)
    return response


@error_decorator('Houve um erro ao criar em conversion')
def create_conversion(id: str) -> HTTPResponse:
    data = {'id': id}

    response = post('/conversions', data)

    return response


@error_decorator('Houve um erro ao atualizar o status em conversion')
def update_conversion(id: str, status: str) -> HTTPResponse:
    data = {'updated_at': 'now()', 'status': status}

    response = path(f'/conversions?id=eq.{id}', data)

    return response


def check_dll(layout_id: str) -> HTTPResponse:
    try:
        response = http.request(
            'GET',
            BASE_DLL_URL + f'/layout/{layout_id}',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )

        return response
    except Exception as e:
        logger.exception(
            f'Erro na requisição /layout: {e}',
            extra={'BASE_URL': BASE_DLL_URL, 'where': f'/layout/{layout_id}'},
            stack_info=True,
        )
        raise e


def process_dll(layout_id: str, file: str) -> HTTPResponse:
    try:
        with open(file, 'rb') as f:
            content = f.read()

        response = http.request(
            'POST',
            BASE_DLL_URL + f'/convert/layout/{layout_id}',
            fields={'file': (file, content, 'text/plain')},
        )

        return response
    except Exception as e:
        logger.exception(
            f'Erro na requisição /convert/layout: {e}',
            extra={'BASE_URL': BASE_DLL_URL, 'where': f'/layout/{layout_id}'},
            stack_info=True,
        )
        raise e
