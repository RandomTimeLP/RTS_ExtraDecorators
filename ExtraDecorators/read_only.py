import inspect,os
def read_only(func):
    def wrapper(self, name, value):
        # Get the current frame
        current_frame = inspect.currentframe()
        # Get the previous frame (the caller)
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller_filename = caller_frame[1][1]
        # Get the filename where the function was defined
        func_filename = inspect.getfile(func)

        # If it's a function, check if it's called from within its file
        if func.__name__ == "__setattr__" and os.path.abspath(caller_filename) != os.path.abspath(func_filename):
            raise Exception(f"Cannot write to read-only attribute {name}")

        return func(self, name, value)
    return wrapper