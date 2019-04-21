from __future__ import division, print_function
import time
from tfmini import TFmini

# create the sensor and give it a port and (optional) operating mode
tf = TFmini('/dev/ttyAMA0', mode=TFmini.STD_MODE)

try:
    print('='*25)
    while True:
        d = tf.read()
        if d:
            print(d)
        else:
            print('No valid response')
        time.sleep(0.01)

except KeyboardInterrupt:
    tf.close()
