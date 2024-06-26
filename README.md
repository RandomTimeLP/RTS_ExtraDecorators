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

```



### @read_only and @restoreAttributeTypeIntegrity
ment to be used on and in the __setattr__ methode in a class
```py
from ExtraDecorators.validatetyping import validatetyping
from ExtraDecorators.read_only import read_only
from ExtraDecorators.restoreAttributeTypeIntegrity import restoreAttributeTypeIntegrity

class Example:
    viewercount:int 
    channelDisplayName:str
    profileImage:any
    @validatetyping
    def __init__(self,channelobject:dict):
        self.viewercount = channelobject.get('viewercount')
        self.channelDisplayName = channelobject.get('channelDisplayName')
        self.profileImage = channelobject.get("image")
    
    @read_only
    def __setattr__(self, name, value) -> None:

        @restoreAttributeTypeIntegrity
        def prepvalid(self,name, value):
            result = (name, value)

            return result

        nam, val = prepvalid(self, name, value)
        print(type(val))
        super().__setattr__(nam, val)

    @validatetyping #from above to ensure there is only a string entered
    def setChannelDisplayname(self, name:str):
        #do some fancy api stuff
        # and get, for some reason an int as channelDisplayname back
        self.channelDisplayName = 125684576623366 #simulated by this hardcoded int

        # this anomaly gets caught by the @restoreAttributeTypeIntegrity decorator and tries to convert the value to a string
        # because self.channelDisplayName was annotated to be a str

# see as i set viewercount as a string, instead of the expected int
channelobject = {'viewercount':'5','channelDisplayName':'test', 'image':'hallo.png'}
# however as you may observe the print statement in the __setattr__ method prints the type of the viewercount value to be an int

cla = Example(channelobject=channelobject)
#cla.viewercount = 5 # failes due to read_only
#print(cla.viewercount) # still prints the value as expected
```
In summery @read_only ensures that you cant just so modify the attributes from outside the class (decorators are an exeption, they can [at least in some cases] still modify the attributes with very little restriction), but still be able to read and compare their values.

And @restoreAtributeTypeIntegrity ensures that, either the incomming value does get changed to the annotated type or it raising an AttributeError if it was unable to restore the type. If type is any or unset it skips the validation process for this atribute.