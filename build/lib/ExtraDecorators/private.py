import inspect,os

def private(func):
    def wrapper(*args, **kwargs):
        # Get the current frame
        current_frame = inspect.currentframe()
        # Get the previous frame (the caller)
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller_filename = caller_frame[1][1]
        # Get the filename where the function was defined
        func_filename = inspect.getfile(func)

        if inspect.ismethod(func):
            # If it's a method, check if it's called from within its class
            if args[0].__class__.__name__ != func.__module__:
                raise Exception(f"Cannot call private method from outside its class")
        else:
            # If it's a function, check if it's called from within its file
            if os.path.abspath(caller_filename) != os.path.abspath(func_filename):
                raise Exception(f"Cannot call private function from outside its file")

        return func(*args, **kwargs)
    return wrapper