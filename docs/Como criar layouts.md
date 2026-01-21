# 🛠 Criando um novo layout

## Criando no layout
1.  Copia o [layout_ref.py](src/converter/layouts/layout_ref.py) dentro da pasta [layout](src/converter/layouts/).
2. Cole dentro de [layout](src/converter/layouts/), e renomeia para o codigo do layout
3.  Defina as informções do layout no `LayoutInfo`.
4.  Na função `processar` implemente a logica de importação do layout.

## Convertendo arquivo

Atualmente tem dois conversores, dar prioridade ao o [pymupdf](src/converter/conversores/pymupdf.py)

Usar a função `extract_text_from_pdf` para converter, isso vai criar um novo arquivo txt com o pdf convertido.

Para o txt convertido use o retorno da função `extract_text_from_pdf`, que retorna o diretorio do arquivo

## Percorrendo o arquivo

1. Abrir o arquivo usando o open

`with path_dir.open(mode='r', encoding='utf-8') as file`

2. Criar um Iterator para o arquivo

`it: Iterator[tuple[int, str]] =  enumerate(file)`

3. Fazer o loop

`for _ , linha in it:`

## Observações

O _ seria o index, mas por questões de boas práticas evitar usar o index direto, caso queira pegar a proxa linha use o next(it, None)

Após o loop que percorre o arquivo, usar o `lancamento.salvar()`

Ao final do processamento do arquivo apague os arquivos PDF, e o txt da conversão dentro do finally
