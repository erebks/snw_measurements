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

ax1 = plt.gca()

plt.axis('normal')

ax1.plot(x, y1, 'r')
ax1.set_xlabel('msg')
ax1.set_ylabel('total timestamp', color='r')
ax1.tick_params('y', colors='r')
ax1.grid(True)

ax2 = ax1.twinx()

ax2.plot(x, y2, 'b')
ax2.set_ylabel('mcu timestamp', color='b')
ax2.tick_params('y', colors='b')

#plt.show()
plt.clf()

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

ax1 = plt.gca()

plt.axis('normal')

ax1.plot(x, y1, 'r')
ax1.set_xlabel('msg')
ax1.set_ylabel('total timestamp', color='r')
ax1.tick_params('y', colors='r')
ax1.grid(True)

ax2 = ax1.twinx()

ax2.plot(x, y2, 'b')
ax2.set_ylabel('mcu timestamp', color='b')
ax2.tick_params('y', colors='b')

#plt.show()
plt.clf()

# Print histogram
# Get rid of packet loss

print(y2)

y1 = np.array(y1, float)
y2 = np.array(y2, float)

# Normalize to first value received and pad to ms
y1 = (y1[ y1 < 1000]-y1[0]) * 1000
y2 = (y2[ y2 < (1000*1000)]) - (y2[0])

fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)

axs[0].hist(y1, bins=50)
axs[0].set_xlabel("ms")

axs[1].hist(y2, bins=50)
axs[1].set_xlabel("ms")

plt.show()
plt.clf()

# Show error probability
