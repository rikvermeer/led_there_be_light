#!/usr/bin/python


import random, time
from ledcontroller import *
from fragmentcontroller import *




leds = 260
bts = 3 * leds
arr = [0] * bts

shoulder = range(259, 229, -1)
stud = range(229, 217, -1)
gun1 = range(217, 170, -1)
gun2 = range(170, 130, -1)
barrel = range(130, 110, -1)
nozzle = range(110, 100, -1)
outside = range(100, -1, -1)


a_gen_shoulder = [0] * len(shoulder)
a_gen_stud = [0] * len(stud)

lpd8806 = LedController(520)

fc = FragmentController(lpd8806, 0.01)
f_nozzle = Fragment(len(nozzle), nozzle)
f_gun2 = Fragment(len(gun2), gun2)
fc.addFragment(f_nozzle)
fc.addFragment(f_gun2)

dg = DummyGenerator(f_nozzle, 0.1, 0)
dg1 = DummyGenerator(f_gun2, 0.1, 1)
dg.start()
dg1.start()
fc.start()
