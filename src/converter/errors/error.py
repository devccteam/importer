from functools import wraps
from typing import Callable, ParamSpec, TypeVar

# P representa os parâmetros da função (argumentos)
# R representa o tipo de retorno da função
P = ParamSpec("P")
R = TypeVar("R")

def error_decorator(
    message: str = 'Internal Error',
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except (APIError):
                raise
            except Exception as e:
                raise BaseError(
                    f'Error em: {func.__name__}\n {message}',
                    detail=str(e)
                ) from e

        return wrapper

    return decorator

class BaseError(Exception):
    """Erro base para os erros internos da aplicação"""
    def __init__(self, message: str, detail: str | None = None) -> None:
        super().__init__(message)
        self.detail = detail

class APIError(BaseError):
    """Erros de conexão com outras API"""
