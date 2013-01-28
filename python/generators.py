import sys, time
from threading import *

class Generator:
    fragment = []

    def __init__(self, fragment):
        self.addFragment(fragment)
        print "I am the Gen constructor"
    
    def __str__(self):
        return "Generator"

    def addFragment(self, fragment):
        self.fragment.extend(fragment)

    def write(self):
        #Override me, call me
        pass

class ThreadedGenerator(Generator, Thread):
    def __init__(self, sleeptime, fragment):
        print "I am the Threaded Generator"
        Generator.__init__(self, fragment)
        Thread.__init__(self)
        self.setDaemon(True)
#        super(ThreadedGenerator, self).__init__(fragment)
 #       super(ThreadedGenerator, self).__init__()
        self.sleeptime = sleeptime

    def stop(self):
        self.running = False

    def start(self):
        self.running = True
        Thread.start(self)

    def run(self):
        while(self.running):
            self.write()
            time.sleep(self.sleeptime)

class Over(ThreadedGenerator):
    def __init__(self, sleeptime, fragment):
        super(Over, self).__init__(sleeptime, fragment)

    def write(self):
        print "add"


class GeneratorFactory:
    @staticmethod
    def m1():
        print "static m1"

class ListeningGeneratorFactory(GeneratorFactory):
    @staticmethod
    def m2():
        GeneratorFactory.m1()
        print "static m2"

if __name__ == "__main__":
    a = ListeningGeneratorFactory()
    a.m2()
    ListeningGeneratorFactory.m2()

    d = Over(0.1, [0,0,128])
    d.start()

    generators = []
    generators.append(d)
    try:
        while(True):
            time.sleep(0.01) 
    except KeyboardInterrupt:
        for g in generators:
            g.stop()
            print "stopping: " + str(g)
            g.join()
            print "joining: " + str(g)
        print "EXITING"
        sys.exit(1)

