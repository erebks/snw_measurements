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

# Calculate watermark of sensordata
def calcWatermark(oldData, newData, key=0xa5a5):
    reg = (oldData >> 13) ^ (newData >> 13) ^ key
    return reg

# Calculate phase of sensordata
def calcPhase(oldPhase, newWatermark):
    return (oldPhase ^ (newWatermark & 0x1)) & 0x1

# Extract phase of gw timestamps
def getPhase(deltaTimestamp):
    if deltaTimestamp < 595 or deltaTimestamp > 605:
        return 1
    else:
        return 0

msgs = []
numMsgsLost = 0

# Go through messages and extract info
for element in data:
    msg = {
        "previous_lost": False,
        "lora_msg_id": None,
        "gw_timestamp": None,
        "gw_timestamp_delta": None,
        "mcu_timestamp": None,
        "mcu_timestamp_s": None,
        "mcu_timestamp_delta": None,
        "mcu_timestamp_delta_s": None,
        "calculation": {"watermark": None, "phase": None},
        "extraction": {"phase": None},
    }

    msg["lora_msg_id"] = element["result"]["uplink_message"]["f_cnt"]

    for gw in element["result"]["uplink_message"]["rx_metadata"]:
        if gw["gateway_ids"]["eui"] == "58A0CBFFFE802A21":
            a = gw["time"]
    a = a[:-4]
    a = datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%f")

    msg["gw_timestamp"] = a.timestamp()

    a = element["result"]["uplink_message"]["frm_payload"]
    a = int(base64.b64decode(a).hex(),16) # Convert base64 to hexstring
    a = int(struct.pack("<Q", a).hex(), 16) # Convert to little endian
    msg["mcu_timestamp"] = int( a / 2**32)  # Pad to 32 bit and use [ms]
    msg["mcu_timestamp_s"] = msg["mcu_timestamp"] / 1000

    # Get previous message if possible
    if not len(msgs) == 0:
        preMsg = msgs[-1]
        # Check if a frame was lost
        if (not ((msg["lora_msg_id"] - preMsg["lora_msg_id"]) == 1) ):
            print("{0} frame(s) after ID {1} lost".format((msg["lora_msg_id"] - preMsg["lora_msg_id"])-1, preMsg["lora_msg_id"]))
            msg["previous_lost"] = True
            numMsgsLost += (msg["lora_msg_id"] - preMsg["lora_msg_id"])-1

        elif (preMsg["previous_lost"] == True):
            # Calc time deltas
            msg["gw_timestamp_delta"] = msg["gw_timestamp"] - preMsg["gw_timestamp"]
            msg["mcu_timestamp_delta"] = msg["mcu_timestamp"] - preMsg["mcu_timestamp"]
            msg["mcu_timestamp_delta_s"] = msg["mcu_timestamp_delta"] / 1000

            # Calc watermark
            msg["calculation"]["watermark"] = calcWatermark(preMsg["mcu_timestamp"], msg["mcu_timestamp"])

            # Get extracted phase
            msg["extraction"]["phase"] = getPhase(msg["gw_timestamp_delta"])

        else:
            # Calc time deltas
            msg["gw_timestamp_delta"] = msg["gw_timestamp"] - preMsg["gw_timestamp"]
            msg["mcu_timestamp_delta"] = msg["mcu_timestamp"] - preMsg["mcu_timestamp"]
            msg["mcu_timestamp_delta_s"] = msg["mcu_timestamp_delta"] / 1000

            # Calc watermark and phase
            msg["calculation"]["watermark"] = calcWatermark(preMsg["mcu_timestamp"], msg["mcu_timestamp"])
            msg["calculation"]["phase"] = calcPhase(preMsg["extraction"]["phase"], msg["calculation"]["watermark"])
            msg["extraction"]["phase"] = getPhase(msg["gw_timestamp_delta"])
            if not (msg["calculation"]["phase"] == msg["extraction"]["phase"]):
                print("Calculated and Extracted phases for ID {0} do not match".format(msg["lora_msg_id"]))

    else:
        # First message
        msg["calculation"]["phase"] = 0
        msg["extraction"]["phase"] = 0

    msgs.append(msg)

# Arrange plots
fig, axs = plt.subplots(2,3)

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

ax011 = axs[0][1].twinx()

ax011.plot(list(ele["lora_msg_id"] for ele in msgs), list(ele["mcu_timestamp_delta_s"] for ele in msgs), "b.-")
ax011.set_ylabel('mcu delta timestamp [s]', color='b')
ax011.tick_params('y', colors='b')

# Print histogram
# Get rid of packet loss and
# normalize to first value received and pad to ms
y1 = np.array(list(ele["gw_timestamp_delta"] for ele in msgs), float)
y2 = np.array(list(ele["mcu_timestamp_delta"] for ele in msgs), float)
y1 = ((y1) - 600) * 1000
y2 = ((y2) - 600 * 1000)

axs[0][2].hist(y1, bins=50, color='r')
axs[0][2].set_title("Histogram gateway timestamps")
axs[0][2].set_xlabel("ms")

axs[1][2].hist(y2, bins=50, color='b')
axs[1][2].set_title("Histogram mcu timestamps")
axs[1][2].set_xlabel("ms")

# Show calculations

axs[1][0].text(0, 0, "Packets lost: {0} (of {1} = {2:.2f}%)".format(numMsgsLost, len(msgs), (numMsgsLost/len(msgs))*100))
axs[1][0].text(0, 1, "Jitter: min: {0:.2f}, max: {1:.2f}, avg: {2:.2f}, mean: {3:.2f}".format(np.min(y1),np.max(y1),np.average(y1),np.mean(y1)))

# Show MCU time vs. gateway time deviation
gateway_first_to_last = msgs[-1]["gw_timestamp"] - msgs[0]["gw_timestamp"]
mcu_first_to_last = msgs[-1]["mcu_timestamp_s"] - msgs[0]["mcu_timestamp_s"]

axs[1][0].text(0, 0.5, "Time duration (delta first to last message) gateway {0:.2f} s, MCU {1:.2f} s, diff {2:.2f} s".format(gateway_first_to_last, mcu_first_to_last, abs(gateway_first_to_last-mcu_first_to_last)))


plt.show()
