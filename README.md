
# Converter

API para converter os arquivos e extrair as informações

## 🛠️  Tecnologias Utilizada

- FastAPI
- Celery
- attrs
- redis
- pandas
- pymypdf
- pypdf
- pandas

## ⚙️  Como Instalar e Rodar

### Atenção
#### Requisitos para rodar o projeto:

- git
- Docker/podman
- uv

### 1° Baixar o projeto
```bash
git clone https://github.com/devccteam/importer
cd converter
```
### 2° Baixar dependências e configurar
```bash
uv sync
```
Configurar o .env, com base no src/converter/.env.exemple

### 3° Rodar o projeto
```
uv run task docker-watch
```

## 📖  Documentação

Com a API rodando pode acessar:
- Swagger UI: http://127.0.0.1:8000/docs - Para testar os endpoints manualmente.
- Redoc: http://127.0.0.1:8000/redoc - Para uma visualização mais limpa e detalhada

## 📂  Estrutra do projeto
- **[docs/](docs/)**: Outras documentações
	- **[Postman.json](docs/Postman.json)**: Arquivo com os endpoins para importar no Postman
- **[infra/](infra/)**: Arquivos do Dockere `sql` inicial do banco
- **temp/**: Arquivo enviados
- **logs/**: Logs da aplicação
- **[src/converter](src/converter)**: Pasta principal do projeto
	- **[server.py](src/converter/server.py)**: Entrypoing da aplicação
	- **[logging.json](src/converter/logging.json)**: Configuração do Logger
	- **[setting.py](src/conversor/setting.py)**: Arquivo que carrega o que tiver no `.env`
	- **[conversores](src/converter/conversores)**: Onde fica os conversores
	- **[errors](src/converter/errors)**: Wrapper de erros
	- **[layouts](src/converter/layouts)**: Pasta para os layouts, e o que é necessário para eles
		-   **[lancamento.py](src/converter/layouts/lancamento.py)**: Classe base para salvar o que foi extraídodos arquivos
		-   **[layout_info.py](src/converter/layouts/layout_info.py)**: Classe base para criar a informação do layout
		-   **[loader.py](src/converter/layouts/loader.py)**: Arquivo que faz a importação dinâmica layouts
	- **[tasks](src/converter/tasks)**: Configuração e gerenciamento das tarefas que rodam em segundo plano
	- **[uteis](src/converter/uteis)**: Arquivos com funções utilitárias para usar em outros lugares
		-   **[arquivos.py](src/converter/uteis/arquivos.py)**: Contem funções relacionadas a manipulação de arquivos
		-   **[config_logger.py](src/converter/uteis/config_logger.py)**: Faz a configuração do Logger
		-   **[datas.py](src/converter/uteis/datas.py)**: Contem funções relacionadas a manipulação de datas
		-   **[rest.py](src/converter/uteis/rest.py)**: Contem funções de requisições
		-   **[status.py](src/converter/uteis/status.py)**: Contem Enum das respostas que a API pode enviar
		-   **[texto.py](src/converter/uteis/texto.py)**: Contem funções relacionadas a manipulação de texto
		-   **[valores.py](src/converter/uteis/valores.py)**: Contem funções relacionadas a manipulação de valores
