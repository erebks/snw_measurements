import json
import matplotlib.pyplot as plt
import sys
import numpy as np
import copy

#import helper

import mea_11_jitter.analyze
import mea_12_xor_dpsk_10s.analyze
import mea_13_xor_dpsk_20ms.analyze
import mea_14_xor_dpsk_30ms.analyze
import mea_15_xor_dpsk_40ms.analyze
import mea_16_xor_dpsk_50ms.analyze
import mea_17_xor_dpsk_60ms.analyze
import mea_18_xor_dpsk_70ms.analyze
import mea_19_xor_dpsk_100ms.analyze
import analyze

# Ignore NONE in list
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

def plot():
    mea_11 = mea_11_jitter.analyze.analyze(mea_11_jitter.analyze.readMeasurements("mea_11_jitter/out.json"))
    mea_12 = mea_12_xor_dpsk_10s.analyze.analyze(mea_12_xor_dpsk_10s.analyze.readMeasurements("mea_12_xor_dpsk_10s/out.json"))
    mea_13 = mea_13_xor_dpsk_20ms.analyze.analyze(mea_13_xor_dpsk_20ms.analyze.readMeasurements("mea_13_xor_dpsk_20ms/out.json"))
    mea_14 = mea_14_xor_dpsk_30ms.analyze.analyze(mea_14_xor_dpsk_30ms.analyze.readMeasurements("mea_14_xor_dpsk_30ms/out.json"))
    mea_15 = mea_15_xor_dpsk_40ms.analyze.analyze(mea_15_xor_dpsk_40ms.analyze.readMeasurements("mea_15_xor_dpsk_40ms/out.json"))
    mea_16 = mea_16_xor_dpsk_50ms.analyze.analyze(mea_16_xor_dpsk_50ms.analyze.readMeasurements("mea_16_xor_dpsk_50ms/out.json"))
    mea_17 = mea_17_xor_dpsk_60ms.analyze.analyze(mea_17_xor_dpsk_60ms.analyze.readMeasurements("mea_17_xor_dpsk_60ms/out.json"))
    mea_18 = mea_18_xor_dpsk_70ms.analyze.analyze(mea_18_xor_dpsk_70ms.analyze.readMeasurements("mea_18_xor_dpsk_70ms/out.json"))
    mea_19 = mea_19_xor_dpsk_100ms.analyze.analyze(mea_19_xor_dpsk_100ms.analyze.readMeasurements("mea_19_xor_dpsk_100ms/out.json"))

    packetloss = analyze.getPacketLosses()
    ber = analyze.getBER()

    # Print barchart of BER
    plt.bar(range(len(ber[1])), ber[1])
    plt.xticks(range(len(ber[1])), ber[0])
#    plt.axes.Axes.set_xticklabels(ber[0])
#    plt.title("Phases wrongly decoded")
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
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_11["msgs"]), float)
    y2 = ((y2) - mea_11_jitter.analyze.NOMINAL_S) * 1000
    y2 = y2[2:] # Delete first, this is an outlier

    plt.hist(y2, bins=mea_11_jitter.analyze.HIST_BINS, color='b')
#    plt.title("Jitter: Histogram of gateway timestamps")
    plt.xlabel("ms")
    plt.grid(True)
    plt.savefig("hist_jitter.svg")
    plt.show()

    # Print delta of 100ms
    plt.plot(list(ele["lora_msg_id"] for ele in mea_19["msgs"]), list(ele["gw_timestamp_delta"] for ele in mea_19["msgs"]), "b.-")
#    plt.title("100ms: Delta timestamps")
    plt.xlabel('msg')
    plt.ylabel('gateway delta timestamp [s]')
    plt.tick_params('y')
    plt.grid(True)
    plt.savefig("delta_100ms.svg")
    plt.show()

    # Print hist of all
#    fig, axs = plt.subplots(2, 4, figsize=(10,5))
    fig, axs = plt.subplots(2, 4, figsize=(10,4))
    fig.tight_layout(h_pad=2)

    # 20ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_13["msgs"]), float)
    y2 = ((y2) - mea_13_xor_dpsk_20ms.analyze.NOMINAL_S) * 1000
    axs[0][0].hist(y2, bins=mea_13_xor_dpsk_20ms.analyze.HIST_BINS, color='b')
    axs[0][0].set_title("a) 20 ms")
#    axs[0][0].set_xlabel("ms", fontsize=8)

    # 30ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_14["msgs"]), float)
    y2 = ((y2) - mea_14_xor_dpsk_30ms.analyze.NOMINAL_S) * 1000
    axs[0][1].hist(y2, bins=mea_14_xor_dpsk_30ms.analyze.HIST_BINS, color='b')
    axs[0][1].set_title("b) 30 ms")
#    axs[0][1].set_xlabel("ms", fontsize=8)

    # 40ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_15["msgs"]), float)
    y2 = ((y2) - mea_15_xor_dpsk_40ms.analyze.NOMINAL_S) * 1000
    axs[0][2].hist(y2, bins=mea_15_xor_dpsk_40ms.analyze.HIST_BINS, color='b')
    axs[0][2].set_title("c) 40 ms")
#    axs[0][2].set_xlabel("ms", fontsize=8)

    # 50ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_16["msgs"]), float)
    y2 = ((y2) - mea_16_xor_dpsk_50ms.analyze.NOMINAL_S) * 1000
    axs[0][3].hist(y2, bins=mea_16_xor_dpsk_50ms.analyze.HIST_BINS, color='b')
    axs[0][3].set_title("d) 50 ms")
#    axs[0][3].set_xlabel("ms", fontsize=8)

    # 60ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_17["msgs"]), float)
    y2 = ((y2) - mea_17_xor_dpsk_60ms.analyze.NOMINAL_S) * 1000
    axs[1][0].hist(y2, bins=mea_17_xor_dpsk_60ms.analyze.HIST_BINS, color='b')
    axs[1][0].set_title("e) 60 ms")
    axs[1][0].set_xlabel("ms", fontsize=8)

    # 70ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_18["msgs"]), float)
    y2 = ((y2) - mea_18_xor_dpsk_70ms.analyze.NOMINAL_S) * 1000
    axs[1][1].hist(y2, bins=mea_18_xor_dpsk_70ms.analyze.HIST_BINS, color='b')
    axs[1][1].set_title("f) 70 ms")
    axs[1][1].set_xlabel("ms", fontsize=8)

    # 100ms
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_19["msgs"]), float)
    y2 = ((y2) - mea_19_xor_dpsk_100ms.analyze.NOMINAL_S) * 1000
    axs[1][2].hist(y2, bins=mea_19_xor_dpsk_100ms.analyze.HIST_BINS, color='b')
    axs[1][2].set_title("g) 100 ms")
    axs[1][2].set_xlabel("ms", fontsize=8)

    # 10 s
    y2 = np.array(list(ele["gw_timestamp_delta"] for ele in mea_12["msgs"]), float)
    y2 = ((y2) - mea_12_xor_dpsk_10s.analyze.NOMINAL_S) * 1000
    axs[1][3].hist(y2, bins=mea_12_xor_dpsk_10s.analyze.HIST_BINS, color='b')
    axs[1][3].set_title("h) 10 s")
    axs[1][3].set_xlabel("ms", fontsize=8)
    plt.savefig("hist.svg")
    plt.show()


if __name__ == "__main__":
    plot()
