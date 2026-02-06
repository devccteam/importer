FROM ghcr.io/astral-sh/uv:alpine3.22 AS builder

ENV UV_COMPILE_BYTECODE=1 \
	UV_LINK_MODE=copy \
	UV_PYTHON_PREFERENCE=only-managed \
	UV_NO_DEV=1 \
	UV_PYTHON_INSTALL_DIR=/python

RUN uv python install 3.14.2

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
	--mount=type=bind,source=uv.lock,target=uv.lock \
	--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
	uv sync --frozen --no-install-project

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --frozen ;

################################################################################

FROM ghcr.io/astral-sh/uv:alpine3.22 AS development

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache libstdc++

RUN addgroup -g 1000 python \
	&& adduser -u 1000 -G python -s /bin/ash -D python ;

COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=python:python /app /app

ENV PATH="/app/.venv/bin:${PATH}"

USER python
ENTRYPOINT []
WORKDIR /app
