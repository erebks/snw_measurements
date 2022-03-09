import json
import matplotlib.pyplot as plt
import sys
import numpy as np
import copy

#import helper

import mea_1_jitter.analyze
import mea_2_xor_dpsk.analyze
import mea_3_xor_dpsk_20ms.analyze
import mea_4_xor_dpsk_50ms.analyze
import mea_5_xor_dpsk_100ms.analyze
import mea_6_xor_dpsk_30ms.analyze
import mea_7_xor_dpsk_40ms.analyze
import mea_8_xor_dpsk_60ms.analyze
import mea_9_xor_dpsk_70ms.analyze
import analyze

# Ignore NONE in list
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

def plot():
    mea_1 = mea_1_jitter.analyze.analyze(mea_1_jitter.analyze.readMeasurements("mea_1_jitter/out.json"))
    mea_2 = mea_2_xor_dpsk.analyze.analyze(mea_2_xor_dpsk.analyze.readMeasurements("mea_2_xor_dpsk/220209_xor_dpsk.json"))
    mea_3 = mea_3_xor_dpsk_20ms.analyze.analyze(mea_3_xor_dpsk_20ms.analyze.readMeasurements("mea_3_xor_dpsk_20ms/220219_xor_dpsk_20ms.json"))
    mea_4 = mea_4_xor_dpsk_50ms.analyze.analyze(mea_4_xor_dpsk_50ms.analyze.readMeasurements("mea_4_xor_dpsk_50ms/220220_xor_dpsk_50ms.json"))
    mea_5 = mea_5_xor_dpsk_100ms.analyze.analyze(mea_5_xor_dpsk_100ms.analyze.readMeasurements("mea_5_xor_dpsk_100ms/220221_xor_dpsk_100ms.json"))
    mea_6 = mea_6_xor_dpsk_30ms.analyze.analyze(mea_6_xor_dpsk_30ms.analyze.readMeasurements("mea_6_xor_dpsk_30ms/220223_xor_dpsk_30ms.json"))
    mea_7 = mea_7_xor_dpsk_40ms.analyze.analyze(mea_7_xor_dpsk_40ms.analyze.readMeasurements("mea_7_xor_dpsk_40ms/220224_xor_dpsk_40ms.json"))
    mea_8 = mea_8_xor_dpsk_60ms.analyze.analyze(mea_8_xor_dpsk_60ms.analyze.readMeasurements("mea_8_xor_dpsk_60ms/220225_xor_dpsk_60ms.json"))
    mea_9 = mea_9_xor_dpsk_70ms.analyze.analyze(mea_9_xor_dpsk_70ms.analyze.readMeasurements("mea_9_xor_dpsk_70ms/220226_xor_dpsk_70ms.json"))

    packetloss = analyze.getPacketLosses()
    ber = analyze.getBER()

    # Print barchart of BER
    plt.bar(range(len(ber[1])), ber[1])
    plt.xticks(range(len(ber[1])), ber[0])
#    plt.axes.Axes.set_xticklabels(ber[0])
    plt.title("Phases wrongly decoded")
    plt.ylabel("[%]")
    plt.grid(linestyle='--', axis='y')
    plt.savefig("phase_errors.svg")
    plt.show()

    # Print barchart of packetloss
#    plt.bar(range(len(packetloss[1])), packetloss[1])
#    plt.xticks(range(len(packetloss[1])),packetloss[0])
#  plt.axes.Axes.set_xticklabels(packetloss[0])
#    plt.title("Packetloss")
#    plt.ylabel("[%]")
#    plt.grid(linestyle='--', axis='y')
#    plt.savefig("packetloss.svg")
#    plt.show()

    # Print hist of jitter
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_1["msgs"]), float)
    y2 = ((y2) - mea_1_jitter.analyze.NOMINAL_S) * 1000 - 12

    plt.hist(y2, bins=mea_1_jitter.analyze.HIST_BINS, color='b')
    plt.title("Jitter: Histogram of gateway timestamps")
    plt.xlabel("ms")
    plt.grid(True)
    plt.savefig("hist_jitter.svg")
    plt.show()

    # Print delta of 100ms
    plt.plot(list(ele["lora_msg_id"] for ele in mea_5["msgs"]), list(ele["gw_timestamp_delta"] for ele in mea_5["msgs"]), "b.-")
    plt.title("100ms: Delta timestamps")
    plt.xlabel('msg')
    plt.ylabel('gateway delta timestamp [s]')
    plt.tick_params('y')
    plt.grid(True)
    plt.savefig("delta_100ms.svg")
    plt.show()

    # Print hist of all
    fig, axs = plt.subplots(2, 4, figsize=(10,5))
    fig.tight_layout(h_pad=2)

    # 20ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_3["msgs"]), float)
    y2 = ((y2) - mea_3_xor_dpsk_20ms.analyze.NOMINAL_S) * 1000
    axs[0][0].hist(y2, bins=mea_3_xor_dpsk_20ms.analyze.HIST_BINS, color='b')
    axs[0][0].set_title("a) 20 ms")
    axs[0][0].set_xlabel("ms", fontsize=8)

    # 30ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_6["msgs"]), float)
    y2 = ((y2) - mea_6_xor_dpsk_30ms.analyze.NOMINAL_S) * 1000
    axs[0][1].hist(y2, bins=mea_6_xor_dpsk_30ms.analyze.HIST_BINS, color='b')
    axs[0][1].set_title("b) 30 ms")
    axs[0][1].set_xlabel("ms", fontsize=8)

    # 40ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_7["msgs"]), float)
    y2 = ((y2) - mea_7_xor_dpsk_40ms.analyze.NOMINAL_S) * 1000
    axs[0][2].hist(y2, bins=mea_7_xor_dpsk_40ms.analyze.HIST_BINS, color='b')
    axs[0][2].set_title("c) 40 ms")
    axs[0][2].set_xlabel("ms", fontsize=8)

    # 50ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_4["msgs"]), float)
    y2 = ((y2) - mea_4_xor_dpsk_50ms.analyze.NOMINAL_S) * 1000
    axs[0][3].hist(y2, bins=mea_4_xor_dpsk_50ms.analyze.HIST_BINS, color='b')
    axs[0][3].set_title("d) 50 ms")
    axs[0][3].set_xlabel("ms", fontsize=8)

    # 60ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_8["msgs"]), float)
    y2 = ((y2) - mea_8_xor_dpsk_60ms.analyze.NOMINAL_S) * 1000
    axs[1][0].hist(y2, bins=mea_8_xor_dpsk_60ms.analyze.HIST_BINS, color='b')
    axs[1][0].set_title("e) 60 ms")
    axs[1][0].set_xlabel("ms", fontsize=8)

    # 70ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_9["msgs"]), float)
    y2 = ((y2) - mea_9_xor_dpsk_70ms.analyze.NOMINAL_S) * 1000
    axs[1][1].hist(y2, bins=mea_9_xor_dpsk_70ms.analyze.HIST_BINS, color='b')
    axs[1][1].set_title("f) 70 ms")
    axs[1][1].set_xlabel("ms", fontsize=8)

    # 100ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_5["msgs"]), float)
    y2 = ((y2) - mea_5_xor_dpsk_100ms.analyze.NOMINAL_S) * 1000
    axs[1][2].hist(y2, bins=mea_5_xor_dpsk_100ms.analyze.HIST_BINS, color='b')
    axs[1][2].set_title("g) 100 ms")
    axs[1][2].set_xlabel("ms", fontsize=8)

    # 10 s
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_2["msgs"]), float)
    y2 = ((y2) - mea_2_xor_dpsk.analyze.NOMINAL_S) * 1000
    axs[1][3].hist(y2, bins=mea_2_xor_dpsk.analyze.HIST_BINS, color='b')
    axs[1][3].set_title("h) 10 s")
    axs[1][3].set_xlabel("ms", fontsize=8)
    plt.savefig("hist.svg")
    plt.show()


if __name__ == "__main__":
    plot()
