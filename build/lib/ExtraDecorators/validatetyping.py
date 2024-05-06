import inspect
from functools import wraps


def validatetyping(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        params = sig.parameters
        bound_values = sig.bind(*args, **kwargs).arguments

        for name, value in bound_values.items():
            expected_type = params[name].annotation
            if expected_type is not inspect._empty and not isinstance(value, expected_type):
                raise ValueError(f"Value {value} is not of {expected_type}")

        return func(*args, **kwargs)
    return wrapper