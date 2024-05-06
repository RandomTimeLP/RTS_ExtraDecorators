from typing import Any

def restoreAttributeTypeIntegrity(func):
    def wrapper(self, name, value):
        if hasattr(self, '__annotations__') and name in self.__annotations__:
            annotation = self.__annotations__[name]
            # Überspringe die Typkonversion, wenn der Typ `typing.Any` ist
            if annotation is Any:
                pass
            elif isinstance(annotation, type):
                # Prüfe, ob die Annotation direkt ein Typ ist
                if not isinstance(value, annotation):
                    try:
                        value = annotation(value)
                    except (TypeError, ValueError):
                        raise AttributeError(f"Failed to convert {value} to {annotation}")
                        return
            else:
                # Versuche, den Typnamen in einen Typ umzuwandeln, wenn es sich um einen String handelt
                try:
                    annotation_type = locals().get(annotation, globals().get(annotation, __builtins__.get(annotation)))
                    if annotation_type and not isinstance(value, annotation_type):
                        try:
                            value = annotation_type(value)
                        except (TypeError, ValueError):
                            raise AttributeError(f"Failed to convert {value} to {annotation_type}")
                except KeyError:
                    print(f"Failed to convert {annotation} to a type")
                    return None
        return func(self, name, value)
    return wrapper