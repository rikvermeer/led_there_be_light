from pubsub import pub
from generators import *
from ledcontroller import *
from fragmentcontroller import *
import random

shoulder = range(230, 260, 1)
stud = range(218, 230, 1)
gun1 = range(217, 170, -1)
gun2 = range(170, 130, -1)
barrel = range(130, 110, -1)
nozzle = range(110, 100, -1)

lpd8806 = LedController(520)

fc = FragmentController(lpd8806, 0.01)

f_stud = Fragment(len(stud), stud)
f_shoulder = Fragment(len(shoulder), shoulder)
f_gun1 = Fragment(len(gun1), gun1)
f_gun2 = Fragment(len(gun2), gun2)
f_barrel = Fragment(len(barrel), barrel)
f_nozzle = Fragment(len(nozzle), nozzle)

fc.addFragment(f_stud)
fc.addFragment(f_shoulder)
fc.addFragment(f_gun1)
fc.addFragment(f_gun2)
fc.addFragment(f_barrel)
fc.addFragment(f_nozzle)

g_stud = ThreadedGenerator(0.01, f_stud)
g_shoulder = ThreadedGenerator(0.1, f_shoulder)
g_gun1 = ThreadedGenerator(0.2, f_gun1)
g_gun2 = ThreadedGenerator(0.2, f_gun2)
#g_barrel = ThreadedGenerator(0.1, f_barrel)
g_nozzle = ThreadedGenerator(0.1, f_nozzle)

#g_gun1 = ThreadedGenerator(0.01, f_gun1)
#g_gun2 = ThreadedGenerator(0.01, f_gun2)
#g_barrel = ThreadedGenerator(0.01, f_barrel)
#g_nozzle = ThreadedGenerator(0.01, f_nozzle)

"""Binary counter"""
g_stud.i = 0
g_stud.max = pow(2, g_stud.fragment.size)
def write_stud():
    bin_arr = map(int, bin(g_stud.i)[2:].rjust(g_stud.fragment.size, '0'))
    for i in range(0, g_stud.fragment.size):
        g_stud.fragment.data[i * 3 + 1] = 255 * bin_arr[i]
    g_stud.i += 1
    if g_stud.i == g_stud.max:
        g_stud.stop()
    
#do random stuff
def write_shoulder():
    for i in range(0, g_shoulder.fragment.size):
        if random.randint(0,1) == 0:
            g_shoulder.fragment.data[i * 3] = 0
            g_shoulder.fragment.data[i * 3 + 1] = 128
            g_shoulder.fragment.data[i * 3 + 2] = 128
        else:
            g_shoulder.fragment.data[i * 3] = 0
            g_shoulder.fragment.data[i * 3 + 1] = 128
            g_shoulder.fragment.data[i * 3 + 2] = 0


g_gun1.i = 0
def write_gun1():
    g_gun1.fragment.data[g_gun1.i * 3 + 1] = 255
    g_gun1.fragment.data[g_gun1.i * 3 + 2] = 128
    g_gun1.i += 1
    if g_gun1.i == g_gun1.fragment.size:
        g_gun1.i = 0 


g_gun2.i = g_gun2.fragment.size - 1
def write_gun2():
    g_gun2.fragment.data[g_gun2.i * 3 + 1] = 64
    g_gun2.fragment.data[g_gun2.i * 3 + 2] = 128
    g_gun2.i -= 1
    if g_gun2.i == 0:
        g_gun2.i = g_gun2.fragment.size -1


def write_barrel():
    pass

g_nozzle.i = 0
def write_nozzle():
    time.sleep(1)
    g_nozzle.fragment.data = [0] * g_nozzle.fragment.size * 3
    g_nozzle.fragment.data[g_nozzle.i * 3] = 255
    g_nozzle.i += 1
    if g_nozzle.i == g_nozzle.fragment.size:
        g_nozzle.i = 0
    

g_stud.write = write_stud
g_shoulder.write = write_shoulder
g_gun1.write = write_gun1
g_gun2.write = write_gun2
#g_barrel = write_barrel
g_nozzle.write = write_nozzle


g_stud.start()
g_shoulder.start()
g_gun1.start()
g_gun2.start()
g_nozzle.start()

fc.start()

time.sleep(15)
