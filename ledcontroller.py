import lpd8806

class LedController:
    
    def __init__(self, size):
        self.size = size
        lpd8806.set(8,16000000,0)

    def write (self, data):
        lpd8806.write(data)
        

    def getSize(self):
        return self.size
    
