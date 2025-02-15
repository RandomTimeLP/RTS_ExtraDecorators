import logging

# Logging aktivieren
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

from ExtraDecorators.validateAttributeType import validateAttributeType

# Test-Klasse mit Typvalidierung
@validateAttributeType()
class Example:
    name: str  # ✅ Wird erkannt & geprüft
    active: bool  # ✅ Wird erkannt & geprüft
    untyped = "this is ignored"  # ❌ Hat keine Annotation → Ignoriert

    def __init__(self, name: str, age: int, active: bool, data: dict):
        self.name = name  # ✅ Wird geprüft (da in Klasse annotiert)
        self.age = age  # ✅ Wird geprüft (da in __init__ annotiert)
        self.active = active  # ✅ Wird geprüft
        self.data = data  # ✅ Wird geprüft
        self.untyped2 = "also ignored"  # ❌ Keine Annotation → Ignoriert

# ✅ Erlaubte Zuweisungen
obj = Example("John", 30, True, {"key": "value"})

obj.age = 25  # ✅ Allowed
obj.data = {"new": "info"}  # ✅ Allowed
obj.untyped = 9999  # ✅ Allowed (da `Any`)

# ❌ Fehlerhafte Zuweisungen
try:
    obj.age = "thirty"  # ❌ TypeError
except TypeError as e:
    print(e)

try:
    obj.active = "yes"  # ❌ TypeError
except TypeError as e:
    print(e)
