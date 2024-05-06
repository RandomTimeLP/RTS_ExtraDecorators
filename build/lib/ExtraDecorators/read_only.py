import inspect,os
def read_only(func):
    def wrapper(self, name, value):
        # Überprüfen, ob der aktuelle Aufruf von einer anderen Klasse kommt
        caller_class = inspect.currentframe().f_back.f_locals.get('self').__class__
        current_class = self.__class__
        if caller_class != current_class:
            # Überprüfen, ob der Aufrufer einen aktiven Decorator ist
            if inspect.isfunction(func) and hasattr(func, '__closure__'):
                closures = func.__closure__
                for closure in closures:
                    if isinstance(closure.cell_contents, type(wrapper)):
                        return func(self, name, value)  # Bypass für aktive Decoratoren
            raise Exception(f"Cannot write to read-only attribute {name}")

        return func(self, name, value)
    return wrapper