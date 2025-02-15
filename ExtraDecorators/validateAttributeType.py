import inspect
import logging
from typing import get_type_hints

logger = logging.getLogger(__name__)  # Logger für dieses Modul

def validateAttributeType():
    """Decorator that enforces type annotations for attributes.
    
    - If an attribute has a type annotation, only values of that type are allowed.
    - Attributes without an annotation are treated as `Any` (no restriction).
    - Supports attributes defined inside `__init__` and at the class level.
    - Raises `TypeError` if an invalid type is assigned.
    """
    
    def decorator(cls):
        if not isinstance(cls, type):  # Ensure decorator is applied to a class
            logger.debug("⚠️ Redundant decoration detected, validateAttributeType can only be used on classes.")
            return cls  # Return the original object unchanged

        # 🔍 Erfasse Typannotationen aus `__init__` und der Klasse
        class_type_hints = get_type_hints(cls)

        # Falls `__init__` existiert, holt es sich die Typen aus den Parametern
        init_type_hints = get_type_hints(cls.__init__) if hasattr(cls, "__init__") else {}
        init_type_hints.pop("self", None)  # `self` ist irrelevant für unsere Prüfung

        # 🔥 Alle bekannten Attribute mit Typen kombinieren
        attribute_types = {**class_type_hints, **init_type_hints}

        class Wrapped(cls):
            def __setattr__(self, key, value):
                stack = inspect.stack()

                # 🔍 Hole Datei & Zeilennummer für bessere Debug-Logs
                caller_frame = stack[1]  # Der direkte Aufrufer von `obj.attr = value`
                caller_file = caller_frame.filename
                caller_line = caller_frame.lineno

                # 🔍 Prüfen, ob das Attribut eine bekannte Typannotation hat
                expected_type = attribute_types.get(key, None)

                # Falls kein Typ bekannt ist → Ignorieren (Behandlung als `Any`)
                if expected_type is None:
                    super().__setattr__(key, value)
                    return

                # 🔥 Typprüfung: Ist der Wert nicht vom erwarteten Typ? → BLOCKIEREN
                if not isinstance(value, expected_type):
                    logger.debug(f"⛔ BLOCKED: Type mismatch for '{key}' at {caller_file}:{caller_line} (Expected: {expected_type}, Got: {type(value)})")
                    raise TypeError(f"Cannot assign value of type {type(value).__name__} to attribute '{key}' (Expected: {expected_type.__name__})")

                logger.debug(f"✅ Allowed: Attribute '{key}' correctly assigned with type {expected_type} at {caller_file}:{caller_line}")
                super().__setattr__(key, value)

        return Wrapped

    return decorator
