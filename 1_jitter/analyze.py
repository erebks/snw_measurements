import json
import matplotlib.pyplot as plt
import base64
import sys
import struct
import datetime
import numpy as np

if (len(sys.argv) < 2):
    print("Too less arguments!")
    print("Use: python3 {0} in_file.json".format(sys.argv[0]))
    exit(1)

in_file = open(sys.argv[1], "r")
data = json.loads(in_file.read())
in_file.close()

# Arrange plots
fig, axs = plt.subplots(2,2)

# Print x-y diagram of absolute timestamps
x = range(len(data))
y1 = []
y2 = []
for element in data:
    a = element["result"]["uplink_message"]["rx_metadata"][0]["time"]
    a = a[:-4]
    a = datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%f")
    y1.append(a)
    # Convert to timestamp
    a = element["result"]["uplink_message"]["frm_payload"]
    a = int(base64.b64decode(a).hex(),16) # Convert base64 to hexstring
    a = int(struct.pack("<Q", a).hex(), 16) # Convert to little endian
    y2.append(int( a / 2**32)) # Pad to 32 bit

axs[0][0].plot(x, y1, 'r')
axs[0][0].set_title("Absolute timestamps")
axs[0][0].set_xlabel('msg')
axs[0][0].set_ylabel('total timestamp', color='r')
axs[0][0].tick_params('y', colors='r')
axs[0][0].grid(True)

ax002 = axs[0][0].twinx()

ax002.plot(x, y2, 'b')
ax002.set_ylabel('mcu timestamp', color='b')
ax002.tick_params('y', colors='b')

# Print x-y diagram of delta timestamps
x = range(len(data)-1)
ts1 = []
y1 = []
ts2 = []
y2 = []
for element in data:
    a = element["result"]["uplink_message"]["rx_metadata"][0]["time"]
    a = a[:-4] # Strip timestamp a bit
    a = float(datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%f").timestamp())
    ts1.append(a)
    if len(ts1) > 1:
        y1.append(ts1[-1]-ts1[-2])
    # Convert to timestamp
    a = element["result"]["uplink_message"]["frm_payload"]
    a = int(base64.b64decode(a).hex(),16) # Convert base64 to hexstring
    a = int(struct.pack("<Q", a).hex(), 16) # Convert to little endian
    ts2.append(int( a / 2**32))
    if len(ts2) > 1:
        y2.append(ts2[-1]-ts2[-2])

axs[1][0].plot(x, y1, 'r')
axs[1][0].set_title("Delta timestamps (Without packet losses)")
axs[1][0].set_xlabel('msg')
axs[1][0].set_ylabel('total timestamp', color='r')
axs[1][0].tick_params('y', colors='r')
axs[1][0].grid(True)

ax012 = axs[1][0].twinx()

ax012.plot(x, y2, 'b')
ax012.set_ylabel('mcu timestamp', color='b')
ax012.tick_params('y', colors='b')

# Print histogram
# Get rid of packet loss

y1 = np.array(y1, float)
y2 = np.array(y2, float)

# Normalize to first value received and pad to ms
y1 = (y1[ y1 < 1000]-y1[0]) * 1000
y2 = (y2[ y2 < (1000*1000)]) - (y2[0])

axs[0][1].hist(y1, bins=50)
axs[0][1].set_title("Histogram gateway timestamps (Without packet losses)")
axs[0][1].set_xlabel("ms")

axs[1][1].hist(y2, bins=50)
axs[1][1].set_title("Histogram mcu timestamps (Without packet losses)")
axs[1][1].set_xlabel("ms")

plt.show()

# Show error probability
