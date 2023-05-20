import os
import time

os.system('echo gpio | sudo tee /sys/class/leds/ACT/trigger')
for j in range(10):
  os.system('echo 1 | sudo tee /sys/class/leds/ACT/brightness') # led on
  time.sleep(1)
  os.system('echo 0 | sudo tee /sys/class/leds/ACT/brightness') # led ooff
  time.sleep(1)
