import json
from time import time

from celery import Celery, Task

from converter.layouts.loader import (
    check_if_layout_file_exists,
    obter_processador,
)
from converter.settings import settings
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo
from converter.uteis.rest import (
    create_conversion,
    process_dll,
    update_conversion,
)

redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT

broker = f'redis://{redis_host}:{redis_port}/0'

celery = Celery('tasks', broker=broker, backend=broker)


logger = config_logger.setup('app.tasks')


@celery.task(bind=True, name='processa', time_limit=3600)
def call_layout(self: Task, layout_id: str, file_obj: Arquivo) -> None:
    id: str = ''
    try:
        id = self.request.id

        create_conversion(id)

        file_obj = Arquivo(**file_obj)

        prc = obter_processador(str(layout_id))

        update_conversion(id, 'Running')
        logger.info(
            f'[Iniciando] task: {id}, name_file: {file_obj.file_dir.name}'
        )

        start_process = time()
        prc(id, file_obj)
        end_process = time()

        update_conversion(id, 'Finished')
        logger.info(
            f'[Finalizou] task: s{id}, name_file: {file_obj.file_dir.name}',
            extra={'Tempo total': f'{end_process - start_process:.2f}s'},
        )

    except Exception as e:
        update_conversion(id, 'Error')
        logger.exception(f'Erro na conversão: {id}', stack_info=True)
        raise Exception(f'Erro na execução da função do {layout_id}.py') from e


def processa_arquivo(layout_id: str, file_obj: Arquivo) -> str:
    try:
        if check_if_layout_file_exists(layout_id):
            task = call_layout.delay(layout_id, file_obj.model_dump())
            return task.id

        data = process_dll(layout_id, str(file_obj.file_dir)).data

        try:
            result = json.loads(data.decode('utf-8'))
        except json.JSONDecodeError:
            result = data.decode('utf-8')
        except UnicodeDecodeError as e:
            logger.exception(f'Erro ao converter a resposta da api para json: {e}')
            raise e

        return result['id']
    finally:
        file_obj.file_dir.unlink()



if __name__ == '__main__':
    celery()
