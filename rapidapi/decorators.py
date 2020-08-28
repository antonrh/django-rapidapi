from typing import Callable


def compose_decorators(*decorators) -> Callable:
    def decorator(func: Callable):
        for dec in reversed(decorators):
            func = dec(func)
        return func

    return decorator
