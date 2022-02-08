import json
import matplotlib.pyplot as plt
import base64
import sys
import struct
import datetime
import numpy as np
import copy

if (len(sys.argv) < 2):
    print("Too less arguments!")
    print("Use: python3 {0} in_file.json".format(sys.argv[0]))
    exit(1)

in_file = open(sys.argv[1], "r")
data = json.loads(in_file.read())
in_file.close()

# Arrange plots
fig, axs = plt.subplots(2,3)

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

gateway_first_to_last = int((y1[-1].timestamp() - y1[0].timestamp())*1000)
mcu_first_to_last = y2[-1]-y2[0]

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

axs[0][1].plot(x, y1, 'r')
axs[0][1].set_title("Delta timestamps")
axs[0][1].set_xlabel('msg')
axs[0][1].set_ylabel('gateway delta timestamp [s]', color='r')
axs[0][1].tick_params('y', colors='r')
axs[0][1].grid(True)

ax011 = axs[0][1].twinx()

ax011.plot(x, y2, 'b')
ax011.set_ylabel('mcu delta timestamp [ms]', color='b')
ax011.tick_params('y', colors='b')

# Print delta timestamps without packet losses

axs[1][1].plot(x, y1, 'r')
axs[1][1].set_title("Delta timestamps (Without packet losses)")
axs[1][1].set_xlabel('msg')
axs[1][1].set_ylabel('gateway delta timestamp [s]', color='r')
axs[1][1].tick_params('y', colors='r')
axs[1][1].grid(True)
axs[1][1].set_ylim([599.9, 600.1])

ax011 = axs[1][1].twinx()
ax011.plot(x, y2, 'b')
ax011.set_ylabel('mcu delta timestamp [ms]', color='b')
ax011.tick_params('y', colors='b')
ax011.set_ylim([599975, 600025])

# Print histogram
# Get rid of packet loss and
# normalize to first value received and pad to ms
y1 = np.array(y1, float)
y2 = np.array(y2, float)
y1a = copy.deepcopy(y1)
y2a = copy.deepcopy(y2)
y1a = (y1a[ y1a < 1000]) * 1000 - 600*1000
y2a = (y2a[ y2a < (1000*1000)]) - 600*1000

axs[0][2].hist(y1a, bins=50)
axs[0][2].set_title("Histogram gateway timestamps (Without packet losses)")
axs[0][2].set_xlabel("ms")

axs[1][2].hist(y2a, bins=50)
axs[1][2].set_title("Histogram mcu timestamps (Without packet losses)")
axs[1][2].set_xlabel("ms")

# Show calculations

axs[1][0].text(0, 0, "Packets lost: {0} ({1}%)".format(len(np.where(y1>1000)[0]),(len(np.where(y1>1000)[0])/len(y1))*100))
axs[1][0].text(0, 1, "Jitter: min: {0}, max: {1}, avg: {2}, mean: {3}".format(np.min(y1),np.max(y1),np.average(y1),np.mean(y1)))

# Show MCU time vs. gateway time deviation
axs[1][0].text(0, 0.5, "Time duration (delta first to last message) gateway {0} ms, MCU {1} ms, diff {2} ms".format(gateway_first_to_last, mcu_first_to_last, abs(gateway_first_to_last-mcu_first_to_last)))

plt.show()
