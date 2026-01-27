from datetime import date
from decimal import Decimal
from typing import Any

from attr import define, field, validators

from converter.settings import settings
from converter.uteis import config_logger, rest

chunk_to_post = settings.CHUNK_TO_POST

logger = config_logger.setup('app.uteis')


@define
class Lancamento:
    _lancamentos: list[dict[str, Any]] = field(factory=list)
    id_task: str = field(default='')
    index: int = field(default=0, validator=validators.instance_of(int))
    cd: str | None = field(default=None, validator=validators.in_(['D', 'C', None]))
    cd1: str | None = field(default=None, validator=validators.in_(['D', 'C', None]))
    cd2: str | None = field(default=None, validator=validators.in_(['D', 'C', None]))
    cd3: str | None = field(default=None, validator=validators.in_(['D', 'C', None]))
    data: date | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(date)),
    )
    data1: date | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(date)),
    )
    data2: date | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(date)),
    )
    data3: date | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(date)),
    )
    numdoc: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    numdoc1: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    numdoc2: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    numdoc3: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    valor: Decimal | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(Decimal)),
    )
    valor1: Decimal | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(Decimal)),
    )
    valor2: Decimal | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(Decimal)),
    )
    valor3: Decimal | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(Decimal)),
    )
    acrescimo: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    juros: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    multa: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    desconto: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    devolucao: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    despesa: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    outros: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    abatimento: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    bonificacao: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    iof: Decimal = field(default=Decimal(0), validator=validators.instance_of(Decimal))
    mora: Decimal = field(default=Decimal(0), validator=validators.instance_of(Decimal))
    seguro: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    tarifa: Decimal = field(
        default=Decimal(0), validator=validators.instance_of(Decimal)
    )
    hist: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    hist1: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    hist2: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    hist3: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    complemento: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    parcela: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    banco: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    filial: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    fornecedor: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    cpfcnpj_fornecedor: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    especie: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    serie: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    inf_adicional: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    inf_adicional3: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    conta_debito: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    conta_credito: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    conta_reduzida: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    conta_completa: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    conta_descricao: str | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )

    def Novo(self) -> None:
        self.cd = None
        self.cd1 = None
        self.cd2 = None
        self.cd3 = None
        self.data = None
        self.data1 = None
        self.data2 = None
        self.data3 = None
        self.numdoc = None
        self.numdoc1 = None
        self.numdoc2 = None
        self.numdoc3 = None
        self.valor = None
        self.valor1 = None
        self.valor2 = None
        self.valor3 = None
        self.acrescimo = Decimal(0)
        self.juros = Decimal(0)
        self.multa = Decimal(0)
        self.desconto = Decimal(0)
        self.devolucao = Decimal(0)
        self.despesa = Decimal(0)
        self.outros = Decimal(0)
        self.abatimento = Decimal(0)
        self.bonificacao = Decimal(0)
        self.iof = Decimal(0)
        self.mora = Decimal(0)
        self.seguro = Decimal(0)
        self.tarifa = Decimal(0)
        self.hist = None
        self.hist1 = None
        self.hist2 = None
        self.hist3 = None
        self.complemento = None
        self.parcela = None
        self.banco = None
        self.filial = None
        self.fornecedor = None
        self.cpfcnpj_fornecedor = None
        self.especie = None
        self.serie = None
        self.inf_adicional = None
        self.inf_adicional3 = None
        self.conta_debito = None
        self.conta_credito = None
        self.conta_reduzida = None
        self.conta_completa = None
        self.conta_descricao = None

    def incluir(self) -> None:
        self._lancamentos.append(
            {
                'conversions_id': self.id_task,
                'index': self.index,
                'cd': {
                    'cd': self.cd,
                    'cd1': self.cd1,
                    'cd2': self.cd2,
                    'cd3': self.cd3,
                },
                'complement': self.complemento,
                'dates': {
                    'data': self.data.isoformat() if self.data else None,
                    'data1': self.data1.isoformat() if self.data1 else None,
                    'data2': self.data2.isoformat() if self.data2 else None,
                    'data3': self.data3.isoformat() if self.data3 else None,
                },
                'descriptions': {
                    'hist': self.hist,
                    'hist1': self.hist1,
                    'hist2': self.hist2,
                    'hist3': self.hist3,
                },
                'documents': {
                    'numdoc': self.numdoc,
                    'numdoc1': self.numdoc1,
                    'numdoc2': self.numdoc2,
                    'numdoc3': self.numdoc3,
                },
                'parcel': self.parcela,
                'supplier': self.fornecedor,
                'identification_supplier': self.cpfcnpj_fornecedor,
                'bank': self.banco,
                'branch': self.filial,
                'type': self.especie,
                'series': self.serie,
                'additional_information': self.inf_adicional,
                'additional_information_add': self.inf_adicional3,
                'values': {
                    'valor': str(self.valor) if self.valor else None,
                    'valor1': str(self.valor1) if self.valor1 else None,
                    'valor2': str(self.valor2) if self.valor2 else None,
                    'valor3': str(self.valor3) if self.valor3 else None,
                },
                'increase': str(self.acrescimo),
                'interest': str(self.juros),
                'fine': str(self.multa),
                'discount': str(self.desconto),
                'return': str(self.devolucao),
                'expense': str(self.despesa),
                'other': str(self.outros),
                'rebate': str(self.abatimento),
                'bonus': str(self.bonificacao),
                'iof': str(self.iof),
                'mora': str(self.mora),
                'insurance': str(self.seguro),
                'rate': str(self.tarifa),
                'debit_account': self.conta_debito,
                'credit_account': self.conta_credito,
                'reduced_account': self.conta_reduzida,
                'full_account': self.conta_completa,
                'account_description': self.conta_descricao,
            }
        )

        self.index = self.index + 1

        if len(self._lancamentos) >= chunk_to_post:
            self.salvar()

    def salvar(self) -> None:
        try:
            rest.insert_releases(self._lancamentos)
            self._lancamentos.clear()
        except Exception as e:
            logger.exception(
                f'Erro ao chamar função que salva no banco:\n {e}',
                extra={'id_task': self.id_task},
                stack_info=True,
            )
            raise Exception('Erro ao tentar salvar no banco') from e
