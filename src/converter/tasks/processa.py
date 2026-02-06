from time import time
from typing import Any

from celery import Task

from converter.layouts.loader import check_if_layout_file_exists, get_instance_layout
from converter.tasks.config import celery
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo
from converter.uteis.rest import (
    create_conversion,
    process_dll,
    update_conversion,
)

logger = config_logger.setup('app.tasks')


@celery.task(bind=True, name='processa', time_limit=3600)
def call_layout(self: Task, layout_id: str, file_data: dict[str, Any]) -> None:
    id_task: str = ''
    try:
        id_task = self.request.id

        file_obj = Arquivo.model_validate(file_data)

        layout = get_instance_layout(layout_id)

        update_conversion(id_task, 'Running')
        logger.info(f'[Iniciando] task: {id_task}, name_file: {file_obj.file_dir.name}')

        start_process = time()
        layout.processar(id_task, file_obj)
        end_process = time()

        update_conversion(id_task, 'Finished')
        logger.info(
            f'[Finalizou] task: {id_task}, name_file: {file_obj.file_dir.name}',
            extra={'Tempo total': f'{end_process - start_process:.2f}s'},
        )

    except Exception as e:
        update_conversion(id_task, 'Error')
        logger.exception(f'Erro na conversão: {id_task}', stack_info=True)
        raise Exception(f'Erro na execução da função do {layout_id}.py') from e


def processa_arquivo(layout_id: str, file_obj: Arquivo) -> str:
    if check_if_layout_file_exists(layout_id):
        task = call_layout.delay(layout_id, file_obj.model_dump(mode='json'))
        create_conversion(task.id)
        return task.id

    data = process_dll(layout_id, file_obj)

    return data['id']
