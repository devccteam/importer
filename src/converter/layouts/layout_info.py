from attr import define, field


@define
class CampoLayout:
    titulo: str
    campo: str
    solinput: bool = field(default=False)
    inputtitle: str = field(default='')
    inputrot: str = field(default='')

    def to_dict(self) -> dict:
        return {
            'titulo': self.titulo,
            'campo': self.campo,
            'solinput': self.solinput,
            'inputtitle': self.inputrot,
            'rotulo': self.inputrot,
        }


@define
class LayoutInfo:
    tipo: str
    descricao: str
    detalhe: str
    datas: list[CampoLayout] = field(factory=list)
    numdocs: list[CampoLayout] = field(factory=list)
    valores: list[CampoLayout] = field(factory=list)
    historicos: list[CampoLayout] = field(factory=list)
    solicitapassword: bool = field(default=False)
    solicitainput: bool = field(default=False)
    tituloinput: str = field(default='')

    def AsJson(self) -> dict:
        dados = {
            'tipo': self.tipo,
            'descricao': self.descricao,
            'detalhe': self.detalhe,
            'solicitapassword': self.solicitapassword,
            'solicitainput': self.solicitainput,
            'tituloinput': self.tituloinput,
        }

        if self.datas:
            dados['datas'] = [data.to_dict() for data in self.datas]

        if self.numdocs:
            dados['numdocs'] = [numdoc.to_dict() for numdoc in self.numdocs]

        if self.valores:
            dados['valores'] = [valor.to_dict() for valor in self.valores]

        if self.historicos:
            dados['historicos'] = [
                historico.to_dict() for historico in self.historicos
            ]

        return dados

    def InsereCampoData(
        self,
        vTitulo: str,
        vCampo: str,
        SolValue: bool = False,
        ValTitle: str = '',
        ValRot: str = '',
    ) -> None:
        self.datas.append(
            CampoLayout(vTitulo, vCampo, SolValue, ValTitle, ValRot)
        )

    def InsereCampoNumDoc(self, vTitulo: str, vCampo: str) -> None:
        self.numdocs.append(CampoLayout(vTitulo, vCampo))

    def InsereCampoValor(self, vTitulo: str, vCampo: str) -> None:
        self.valores.append(CampoLayout(vTitulo, vCampo))

    def InsereCampoHist(self, vTitulo: str, vCampo: str) -> None:
        self.historicos.append(CampoLayout(vTitulo, vCampo))
