from abc import ABC, abstractmethod

from converter.layouts.layout_info import LayoutInfo
from converter.uteis.arquivos import Arquivo


class LayoutBase(ABC):
    layout: LayoutInfo

    def info_layout(self) -> dict[str, str]:
        return self.layout.AsJson()

    @abstractmethod
    def processar(self, id_task: str, file_obj: Arquivo) -> None:
        """
        Extrai as informações de um arquivo
        """
