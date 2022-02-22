import json
import matplotlib.pyplot as plt
import sys
import numpy as np
import copy

sys.path.append('../')

# importing
import helper

# Ignore NONE in list
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

PRINT_MATCHES = False
NOMINAL_S = 300
TOLERANCE_S = 0.010
HIST_BINS = 200

if (len(sys.argv) < 2):
    print("Too less arguments!")
    print("Use: python3 {0} in_file.json".format(sys.argv[0]))
    exit(1)

in_file = open(sys.argv[1], "r")
data = json.loads(in_file.read())
in_file.close()

numMsgsLost, msgs = helper.readMessages(data, NOMINAL_S, TOLERANCE_S, PRINT_MATCHES)

# Arrange plots
fig, axs = plt.subplots(4,4)
fig.suptitle("DPSK 20ms")

# Print x-y diagram of absolute timestamps
axs[0][0].plot(list(ele["lora_msg_id"] for ele in msgs), list(ele["gw_timestamp"] for ele in msgs), "r.-")
axs[0][0].set_title("Absolute timestamps")
axs[0][0].set_xlabel('msg')
axs[0][0].set_ylabel('gateway timestamp [s]', color='r')
axs[0][0].tick_params('y', colors='r')
axs[0][0].grid(True)

ax002 = axs[0][0].twinx()

ax002.plot(list(ele["lora_msg_id"] for ele in msgs), list(ele["mcu_timestamp_s"] for ele in msgs), "b.-")
ax002.set_ylabel('mcu timestamp [s]', color='b')
ax002.tick_params('y', colors='b')

# Print x-y diagram of delta timestamps

axs[0][1].plot(list(ele["lora_msg_id"] for ele in msgs), list(ele["gw_timestamp_delta"] for ele in msgs), "r.-")
axs[0][1].set_title("Delta timestamps")
axs[0][1].set_xlabel('msg')
axs[0][1].set_ylabel('gateway delta timestamp [s]', color='r')
axs[0][1].tick_params('y', colors='r')
axs[0][1].grid(True)

axs[0][2].plot(list(ele["lora_msg_id"] for ele in msgs), list(ele["mcu_timestamp_delta"] for ele in msgs), "b.-")
axs[0][2].set_title("Delta timestamps")
axs[0][2].set_xlabel('msg')
axs[0][2].set_ylabel('mcu delta timestamp [s]', color='b')
axs[0][2].tick_params('y', colors='b')
axs[0][2].grid(True)

# Print histogram
# Get rid of packet loss and
# normalize to first value received and pad to ms
y1 = np.array(list(ele["mcu_timestamp_delta"] for ele in msgs), float)
y2 = np.array(list(ele["gw_timestamp_delta"] for ele in msgs), float)
y3 = np.array(list(ele["nw_timestamp_delta"] for ele in msgs), float)

y1 = ((y1) - NOMINAL_S * 1000)
y2 = ((y2) - NOMINAL_S) * 1000
y3 = ((y3) - NOMINAL_S) * 1000

axs[1][0].hist(y1, bins=HIST_BINS, color='b')
axs[1][0].set_title("Histogram mcu timestamps")
axs[1][0].set_xlabel("ms")

axs[2][0].hist(y2, bins=HIST_BINS, color='r')
axs[2][0].set_title("Histogram gateway timestamps")
axs[2][0].set_xlabel("ms")

axs[3][0].hist(y3, bins=HIST_BINS, color='g')
axs[3][0].set_title("Histogram network timestamps")
axs[3][0].set_xlabel("ms")

# Print detailed histogram
# THIS NEEDS TO BE ADJUSTED FOR EVERY PLOT

# Only TS at 0s
gw_ts = np.array(list(ele["gw_timestamp_delta"] for ele in msgs), float)
gw_ts = (gw_ts - NOMINAL_S) * 1000
gw_ts = gw_ts[gw_ts < 5000]
gw_ts = gw_ts[gw_ts > -100]

axs[2][2].hist(gw_ts, bins=HIST_BINS, color='r')
axs[2][2].set_title("Histogram GW timestamps (@ 0ms)")
axs[2][2].set_xlabel("ms")

# Print detailed histogram

# Only TS at 0s
nw_ts = np.array(list(ele["nw_timestamp_delta"] for ele in msgs), float)
nw_ts = (nw_ts - NOMINAL_S) * 1000
nw_ts = nw_ts[nw_ts < 5000]
nw_ts = nw_ts[nw_ts > -100]

axs[3][2].hist(nw_ts, bins=HIST_BINS, color='g')
axs[3][2].set_title("Histogram NW timestamps (@ 0ms)")
axs[3][2].set_xlabel("ms")

# Show calculations
y1 = []
for ele in msgs:
    if not (ele["gw_timestamp_delta"] == None):
        y1.append(ele["gw_timestamp_delta"]*1000)

y1 = np.array(y1)

print("Packetloss: {0} (of {1} = {2:.2f}%)".format(numMsgsLost, len(msgs), (numMsgsLost/len(msgs))*100))
print("Jitter: min: {0:.2f} ms, max: {1:.2f} ms, avg: {2:.2f} ms, mean: {3:.2f} ms".format(np.min(y1),np.max(y1),np.average(y1),np.mean(y1)))

plt.show()
