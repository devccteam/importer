from typing import Callable


def error_decorator(
    message: str = 'Internal Error',
) -> Callable[..., Callable[..., any]]:
    def decorator(func: Callable[..., any]) -> Callable[..., any]:
        def wrapper(*args: any, **kwargs: any) -> any:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                raise Exception(
                    f'Error em: {func.__name__}\n {message}'
                ) from e

        return wrapper

    return decorator
