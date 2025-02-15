import inspect
import os

class PrivateFunction(Exception):
    """ Exception for unauthorized access to a private function outside its file. """
    def __init__(self, func_name, func_filename, caller_filename, caller_lineno, caller_function):
        self.message = (
            f"🚫 Error: Private function '{func_name}' cannot be called from outside its file!\n"
            f"  📍 Caller: File '{caller_filename}', line {caller_lineno}, function '{caller_function}'\n"
            f"  🔒 Allowed only inside the file '{func_filename}'."
        )
        super().__init__(self.message)

class PrivateClassMethod(Exception):
    """ Exception for unauthorized access to a private class method from outside its class. """
    def __init__(self, class_name, method_name, module_name, caller_filename, caller_lineno, caller_function):
        self.message = (
            f"🚫 Error: Private method '{method_name}' of class '{class_name}' was called from outside!\n"
            f"  📍 Caller: File '{caller_filename}', line {caller_lineno}, function '{caller_function}'\n"
            f"  🔒 Allowed only inside the class '{class_name}' (Module: {module_name})."
        )
        super().__init__(self.message)

def private(func):
    """ Decorator for private functions and methods. 
        - Functions can only be called from within their file.
        - Methods can only be called from within their own class.
    """
    def wrapper(*args, **kwargs):
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)[1]  # Caller frame
        caller_filename = os.path.abspath(caller_frame.filename)  # File of the caller
        caller_lineno = caller_frame.lineno  # Line number of the call
        caller_function = caller_frame.function  # Function name of the caller

        func_filename = os.path.abspath(inspect.getfile(func))  # File where the function is defined

        # Check if it's a method (first argument `self`)
        if inspect.ismethod(func) or (inspect.isfunction(func) and args and hasattr(args[0], '__class__')):
            instance = args[0]
            class_name = instance.__class__.__name__
            method_name = func.__name__

            if instance.__class__.__module__ != func.__module__:
                raise PrivateClassMethod(class_name, method_name, func.__module__, caller_filename, caller_lineno, caller_function)
        
        else:
            # If it's a function, check if it's called from the same file
            if caller_filename != func_filename:
                raise PrivateFunction(func.__name__, func_filename, caller_filename, caller_lineno, caller_function)

        return func(*args, **kwargs)

    return wrapper
