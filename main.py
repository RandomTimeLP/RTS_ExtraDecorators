from ExtraDecorators.validateInputTyping import validateInputTyping

class Example:
    viewercount:int 
    channelDisplayName:str
    @validateInputTyping
    def __init__(self,channelobject:dict):
        
        self.viewercount = channelobject.get('viewercount')
        self.channelDisplayName = channelobject.get('channelDisplayName')
        self.profileImage = channelobject.get("image")
    


    @validateInputTyping #from above to ensure there is only a string entered
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