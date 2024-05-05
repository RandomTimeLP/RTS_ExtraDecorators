import inspect
from functools import wraps

def validatetyping(func):
    """
    A decorator to validate the types of function arguments and class attributes.

    If applied to a function, it validates the types of arguments passed to the function.
    If applied to a class, it validates the types of attributes assigned to the class.

    Args:
    - func: The function to be decorated.

    Returns:
    - A wrapper function that performs type validation.

    Example usage:

    # Example 1: Applying to a function
    @validatetyping
    def add(x: int, y: int) -> int:
        return x + y

    result = add(5, 10)  # Valid call
    result = add(5, '10') # Invalid call, will print an error message

    # Example 2: Applying to a class
    class Point:
        @validatetyping
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

    p = Point(3, 4)  # Valid initialization
    p = Point('3', 4) # Invalid initialization, will print an error message
    """
    if inspect.isfunction(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            params = sig.parameters
            for name, value in list(zip(params, args)) + list(kwargs.items()):
                expected_type = params[name].annotation
                if expected_type is not inspect._empty and not isinstance(value, expected_type):
                    raise ValueError(f"Value {value} is not of {expected_type}")
            return func(*args, **kwargs)
        return wrapper
    else:
        def setattr_wrapper(self, name, value):
            if hasattr(self, '__annotations__') and name in self.__annotations__:
                type_name = self.__annotations__[name]
                try:
                    annotation_type = locals().get(type_name)
                    if annotation_type is None:
                        annotation_type = globals().get(type_name)
                    if annotation_type is None:
                        annotation_type = __builtins__[type_name]
                except KeyError:
                    print(f"Failed to convert {type_name} to a type")
                    return None

                if value is not None:
                    if not isinstance(value, annotation_type):
                        try:
                            value = annotation_type(value)
                        except (TypeError, ValueError):
                            print(f"Failed to convert {value} to {annotation_type}")
                            return
            func(self, name, value)
        return setattr_wrapper