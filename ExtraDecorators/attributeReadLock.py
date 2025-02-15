import inspect
import logging

logger = logging.getLogger(__name__)  # Logger für dieses Modul

def attributeReadLock(allowed_attributes: list[str] = None, strict_mode: bool = True):
    """Decorator that prevents reading of attributes from outside the class, except for allowed ones.
    
    - allowed_attributes: List of attributes that can be read externally.
    - strict_mode=True → Raises AttributeError when accessed from outside.
    - strict_mode=False → Returns None instead of the attribute value.
    """
    
    if allowed_attributes is None:
        allowed_attributes = []  # If no attributes are specified, no attributes are readable

    def decorator(cls):
        if not isinstance(cls, type):  # Ensure decorator is applied to a class
            logger.debug("⚠️ Redundant decoration detected, attributeReadLock can only be used on classes.")
            return cls  # Return the original object unchanged

        class Wrapped(cls):
            def __getattribute__(self, key):
                # 🔍 Falls es ein internes Attribut ist → Ignorieren (kein Logging, keine Sperrung)
                if key.startswith("__") and key.endswith("__"):
                    return super().__getattribute__(key)

                # 🔍 Wert des Attributes holen
                value = super().__getattribute__(key)

                # ✅ Methoden sind IMMER erlaubt
                if callable(value):
                    logger.debug(f"✅ Allowed: Method '{key}' is always accessible")
                    return value

                stack = inspect.stack()
                
                # 🔍 Hole Datei & Zeilennummer für bessere Debug-Logs
                caller_frame = stack[1]  # Der direkte Aufrufer von `obj.attr`
                caller_file = caller_frame.filename
                caller_line = caller_frame.lineno

                logger.debug(f"🔍 Attempting to read '{key}' at {caller_file}:{caller_line}")

                # ✅ Allow reading attributes inside methods of the class
                inside_valid_method = False

                for frame in stack:
                    if "self" in frame.frame.f_locals:
                        caller_instance = frame.frame.f_locals["self"]
                        
                        # Sicherstellen, dass die Methode zur Klasse gehört
                        method_name = frame.function
                        if method_name == "__getattribute__":  # Direkter Attributzugriff -> Blockieren
                            continue
                        
                        method_obj = getattr(self.__class__, method_name, None)

                        if isinstance(caller_instance, self.__class__) and callable(method_obj):
                            # Nur echte Methoden der Klasse erlauben (keine externen Zugriffe)
                            if method_name in dir(self.__class__):
                                logger.debug(f"✅ Allowed: Attribute '{key}' read inside method '{method_name}' at {caller_file}:{caller_line}")
                                inside_valid_method = True
                                break  # Stop at the first valid method
                
                # ✅ Allow reads from within the class
                if inside_valid_method:
                    return value

                # ✅ Allow reads if the attribute is in the allowed list
                if key in allowed_attributes:
                    logger.debug(f"⚠️ Allowed: '{key}' is in the allowed attributes list at {caller_file}:{caller_line}")
                    return value

                # ❌ Block reading for all other attributes
                if strict_mode:
                    logger.debug(f"⛔ BLOCKED: Reading of '{key}' from outside the class at {caller_file}:{caller_line}!")
                    raise AttributeError(f"Reading of attribute '{key}' from outside the class is not allowed!")
                
                logger.debug(f"⚠️ Allowed (Non-Strict Mode): Returning None instead of '{key}' at {caller_file}:{caller_line}")
                return None  # Return None instead of raising an error

        return Wrapped

    return decorator
