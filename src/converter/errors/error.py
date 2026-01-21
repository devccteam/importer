from collections.abc import Callable, Coroutine
from functools import wraps
from http import HTTPStatus
from typing import Any, ParamSpec, TypeVar

# P representa os parâmetros da função (argumentos)
# R representa o tipo de retorno da função
P = ParamSpec('P')
R = TypeVar('R')


def error_decorator(
    message: str = 'Internal Error',
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator para funções sincronas"""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except (APIError, FileError):
                raise
            except Exception as e:
                raise BaseError(message, detail=str(e)) from e

        return wrapper

    return decorator


def async_error_decorator(
    message: str = 'Internal Error',
) -> Callable[
    [Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]
]:
    """Decorator para funções assíncronas."""

    def decorator(
        func: Callable[P, Coroutine[Any, Any, R]],
    ) -> Callable[P, Coroutine[Any, Any, R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return await func(*args, **kwargs)
            except (APIError, FileError):
                raise
            except Exception as e:
                raise BaseError(message=message, detail=str(e)) from e

        return wrapper

    return decorator


class BaseError(Exception):
    """Erro base para os erros internos da aplicação"""

    def __init__(
        self,
        message: str,
        *,
        detail: str | None = None,
        code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail
        self.code = code


class APIError(BaseError):
    """Erros de conexão com outras API"""

    def __init__(
        self,
        message: str = 'Erro de conexão com API externa',
        *,
        detail: str | None = None,
        code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ) -> None:
        super().__init__(message=message, detail=detail, code=code)


class FileError(BaseError):
    """Erros relacionados a arquivos"""

    def __init__(
        self,
        message: str,
        *,
        detail: str | None = None,
        code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ) -> None:
        super().__init__(message, detail=detail, code=code)
