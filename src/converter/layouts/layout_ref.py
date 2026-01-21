from converter.layouts.lancamento import Lancamento
from converter.layouts.layout_base import LayoutBase
from converter.layouts.layout_info import LayoutInfo
from converter.uteis import config_logger
from converter.uteis.arquivos import Arquivo

logger = config_logger.setup('app.layouts')


class Processador(LayoutBase):
    layout = LayoutInfo()

    def processar(self, id_task: str, file_obj: Arquivo) -> None:
        try:
            lancamento = Lancamento(id_task=id_task)
        finally:
            pass
