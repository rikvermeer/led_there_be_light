import lpd8806, time
print lpd8806.set(8, 1000000, 0)
leds = 526
out = [0] * (leds * 3)
for i in range(leds):
    j = 3*i
    out[j] = 0
    out[j+1] = 100
    out[j+2] = 250
lpd8806.write((out))
