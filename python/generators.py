import sys, time
import logging
from threading import *

def log():
    return logging.getLogger("Generator")

"""
Generator
"""
class Generator:
    fragment = []

    def __init__(self, fragment):
        self.addFragment(fragment)
        log().debug("Starting " + str(self))
    
    def __str__(self):
        return "Generator"

    def addFragment(self, fragment):
        self.fragment.extend(fragment)

    def write(self):
        #Override me, call me
        pass


"""
Threaded Generator
"""
class ThreadedGenerator(Generator, Thread):
    def __init__(self, sleeptime, fragment):
        Generator.__init__(self, fragment)
        Thread.__init__(self)
        self.setDaemon(True)
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

    def __str__(self):
        return "ThreadedGenerator"


"""
Test thing
"""
class Over(ThreadedGenerator):
    def __init__(self, sleeptime, fragment):
        ThreadedGenerator.__init__(self, sleeptime, fragment)

    def write(self):
        print "add"

"""
GeneratorFactory generates generaly Generators
"""
class GeneratorFactory:
    @staticmethod
    def m1():
        print "static m1"

"""
Let the GeneratorFactory listen on a port
"""
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

