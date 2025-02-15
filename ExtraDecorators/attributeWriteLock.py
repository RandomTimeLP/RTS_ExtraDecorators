import inspect
import logging

logger = logging.getLogger(__name__)  # Logger für dieses Modul

def attributeWriteLock(allowed_attributes: list[str] = None):
    """Decorator that prevents modification of attributes from outside the class, except for allowed ones."""
    
    if allowed_attributes is None:
        allowed_attributes = []  # If no attributes are specified, all attributes are locked

    def decorator(cls):
        if not isinstance(cls, type):  # Ensure decorator is applied to a class
            logger.debug("⚠️ Redundant decoration detected, attributeWriteLock can only be used on classes.")
            return cls  # Return the original object unchanged

        class Wrapped(cls):
            def __setattr__(self, key, value):
                stack = inspect.stack()
                
                # 🔍 Hole Datei & Zeilennummer für bessere Debug-Logs
                caller_frame = stack[1]  # Der direkte Aufrufer von `obj.attr = value`
                caller_file = caller_frame.filename
                caller_line = caller_frame.lineno

                logger.debug(f"🔍 Attempting to modify '{key}' with value '{value}' at {caller_file}:{caller_line}")

                # ✅ Allow setting attributes inside __init__
                if len(stack) > 1 and stack[1].function == "__init__":
                    logger.debug(f"✅ Allowed: Setting '{key}' inside __init__ at {caller_file}:{caller_line}")
                    super().__setattr__(key, value)
                    return
                
                # 🔹 Check if modification happens within a method of the class
                inside_valid_method = False

                for frame in stack:
                    if "self" in frame.frame.f_locals:
                        caller_instance = frame.frame.f_locals["self"]
                        
                        # Sicherstellen, dass die Methode zur Klasse gehört
                        method_name = frame.function
                        if method_name == "__setattr__":  # Direkter Attributzugriff -> Blockieren
                            continue
                        
                        method_obj = getattr(self.__class__, method_name, None)

                        if isinstance(caller_instance, self.__class__) and callable(method_obj):
                            # Nur echte Methoden der Klasse erlauben (keine externen Zugriffe)
                            if method_name in dir(self.__class__):
                                logger.debug(f"✅ Allowed: Attribute '{key}' modified inside method '{method_name}' at {caller_file}:{caller_line}")
                                inside_valid_method = True
                                break  # Stop at the first valid method
                
                # ✅ Allow modifications from a real method of the class
                if inside_valid_method:
                    super().__setattr__(key, value)
                else:
                    # ❌ Block modification if not in the allowed list
                    if key not in allowed_attributes:
                        logger.debug(f"⛔ BLOCKED: Modification of '{key}' from outside the class at {caller_file}:{caller_line}!")
                        raise AttributeError(f"Modification of attribute '{key}' from outside the class is not allowed!")
                    logger.debug(f"⚠️ Allowed: '{key}' is in the allowed attributes list at {caller_file}:{caller_line}")
                    super().__setattr__(key, value)

        return Wrapped

    return decorator
