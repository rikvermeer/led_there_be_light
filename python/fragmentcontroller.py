from threading import *
import time

class Fragment:
    
    def __init__(self, size, mapping):
        self.mapping = mapping
        self.size = size
        self.data = [0] * (size * 3)

    def getMapping(self):
        return self.mapping
    
    def setData(self, data):
        self.data = data;

    def getData(self):
        return self.data

    def getSize(self):
        return self.size

class DummyGenerator(Thread):
#colors:
    #0 is blue
    #1 is red
    #2 is green

    def __init__ (self, fragment, sleeptime, color):
        Thread.__init__(self)
        self.fragment = fragment
        self.sleeptime = sleeptime
        self.color = color

    def run(self):
        i = 0
        while(True):
            #for i in range(0, self.fragment.getSize()):
            self.fragment.getData()[i*3 + self.color] = 255

            time.sleep(self.sleeptime)
            i += 1
            if i == self.fragment.getSize():
                i = 0

class FragmentController(Thread):
    
    fragments = []

    def __init__ (self, ledcontroller, sleeptime = 0.01):
        Thread.__init__(self)
        self.ledcontroller = ledcontroller
        self.sleeptime = sleeptime

    def addFragment(self, fragment):
        self.fragments.append(fragment)


    def write(self):
        ledsize = self.ledcontroller.getSize()
        data = [0] * (ledsize * 3)

        for fragment in self.fragments:
            #print "writing fragment"
            fragmentData = fragment.getData();
            fragmentMapping = fragment.getMapping();
            #print "data: ", fragmentData
            #print "mapping: ", fragmentMapping
            for i in range(0, len(fragmentMapping)):
                ledposition = fragmentMapping[i]
                data[ledposition * 3] = fragmentData[i * 3] 
                data[ledposition * 3 + 1] = fragmentData[i* 3 + 1]
                data[ledposition * 3 + 2] = fragmentData[i* 3 + 2]
            

        
        self.ledcontroller.write(data)

    def run(self):
        while(True):
            self.write()
            time.sleep(self.sleeptime)


