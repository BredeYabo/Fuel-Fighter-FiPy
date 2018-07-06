#by Sebastian Kleivenes
print("\n\nPycom up and running!\n")
LED(LED_pink_soft)
ts(1)
LED(LED_off)
ts(1)
LED(LED_pink_soft)
ts(1)
LED(LED_off)
ts(1)
if SDMOUNTED==True:
    LED(LED_pink_soft)
    ts(7)
    LED(LED_off)
    execfile('/flash/ULTIMATE.py')
else:
    pass
print("\n\n░░░░░░░░░░░░░░░▄▄░░░░░░░░░░░\n░░░░░░░░░░░░░░█░░█░░░░░░░░░░\n░░░░░░░░░░░░░░█░░█░░░░░░░░░░\n░░░░░░░░░░░░░░█░░█░░░░░░░░░░\n░░░░░░░░░░░░░░█░░█░░░░░░░░░░\n██████▄███▄████░░███▄░░░░░░░\n▓▓▓▓▓▓█░░░█░░░█░░█░░░███░░░░\n▓▓▓▓▓▓█░░░█░░░█░░█░░░█░░█░░░\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░█░░░\n▓▓▓▓▓▓█░░░░░░░░░░░░░░░░█░░░░\n▓▓▓▓▓▓█░░░░░░░░░░░░░░██░░░░░\n▓▓▓▓▓▓█████░░░░░░░░██░░░░░░\n\n")
