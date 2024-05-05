# ExtraDecorators
This module introduces some handy decorators like @validatetyping. 


### @validatetyping
```py
# Example 1: Applying to a function
@validatetyping
def add(x: int, y: int) -> int:
    return x + y

result = add(5, 10)  # Valid call
result = add(5, '10') # Invalid call, will raise an ValueError

# Example 2: Applying to a class
class Point:
    @validatetyping
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

p = Point(3, 4)  # Valid initialization
p = Point('3', 4) # Invalid initialization, will raise an ValueError
```
There are some more in there, but not documentet (WIP)

