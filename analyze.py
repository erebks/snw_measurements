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

# Ignore NONE in list
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

def getPacketLosses():
    packetlosses = [
        [
            "Jitter",
            "10s",
            "20ms",
            "30ms",
            "40ms",
            "50ms",
            "60ms",
            "70ms",
            "100ms",
        ],
        [
            mea_1_jitter.analyze.analyze(mea_1_jitter.analyze.readMeasurements("mea_1_jitter/out.json"))["numMsgsLost"],
            mea_2_xor_dpsk.analyze.analyze(mea_2_xor_dpsk.analyze.readMeasurements("mea_2_xor_dpsk/220209_xor_dpsk.json"))["numMsgsLost"],
            mea_3_xor_dpsk_20ms.analyze.analyze(mea_3_xor_dpsk_20ms.analyze.readMeasurements("mea_3_xor_dpsk_20ms/220219_xor_dpsk_20ms.json"))["numMsgsLost"],
            mea_6_xor_dpsk_30ms.analyze.analyze(mea_6_xor_dpsk_30ms.analyze.readMeasurements("mea_6_xor_dpsk_30ms/220223_xor_dpsk_30ms.json"))["numMsgsLost"],
            mea_7_xor_dpsk_40ms.analyze.analyze(mea_7_xor_dpsk_40ms.analyze.readMeasurements("mea_7_xor_dpsk_40ms/220224_xor_dpsk_40ms.json"))["numMsgsLost"],
            mea_4_xor_dpsk_50ms.analyze.analyze(mea_4_xor_dpsk_50ms.analyze.readMeasurements("mea_4_xor_dpsk_50ms/220220_xor_dpsk_50ms.json"))["numMsgsLost"],
            mea_8_xor_dpsk_60ms.analyze.analyze(mea_8_xor_dpsk_60ms.analyze.readMeasurements("mea_8_xor_dpsk_60ms/220225_xor_dpsk_60ms.json"))["numMsgsLost"],
            mea_9_xor_dpsk_70ms.analyze.analyze(mea_9_xor_dpsk_70ms.analyze.readMeasurements("mea_9_xor_dpsk_70ms/220226_xor_dpsk_70ms.json"))["numMsgsLost"],
            mea_5_xor_dpsk_100ms.analyze.analyze(mea_5_xor_dpsk_100ms.analyze.readMeasurements("mea_5_xor_dpsk_100ms/220221_xor_dpsk_100ms.json"))["numMsgsLost"],
        ]
    ]

    return packetlosses

def getBER():
    mea_2 = mea_2_xor_dpsk.analyze.analyze(mea_2_xor_dpsk.analyze.readMeasurements("mea_2_xor_dpsk/220209_xor_dpsk.json"))
    mea_3 = mea_3_xor_dpsk_20ms.analyze.analyze(mea_3_xor_dpsk_20ms.analyze.readMeasurements("mea_3_xor_dpsk_20ms/220219_xor_dpsk_20ms.json"))
    mea_4 = mea_4_xor_dpsk_50ms.analyze.analyze(mea_4_xor_dpsk_50ms.analyze.readMeasurements("mea_4_xor_dpsk_50ms/220220_xor_dpsk_50ms.json"))
    mea_5 = mea_5_xor_dpsk_100ms.analyze.analyze(mea_5_xor_dpsk_100ms.analyze.readMeasurements("mea_5_xor_dpsk_100ms/220221_xor_dpsk_100ms.json"))
    mea_6 = mea_6_xor_dpsk_30ms.analyze.analyze(mea_6_xor_dpsk_30ms.analyze.readMeasurements("mea_6_xor_dpsk_30ms/220223_xor_dpsk_30ms.json"))
    mea_7 = mea_7_xor_dpsk_40ms.analyze.analyze(mea_7_xor_dpsk_40ms.analyze.readMeasurements("mea_7_xor_dpsk_40ms/220224_xor_dpsk_40ms.json"))
    mea_8 = mea_8_xor_dpsk_60ms.analyze.analyze(mea_8_xor_dpsk_60ms.analyze.readMeasurements("mea_8_xor_dpsk_60ms/220225_xor_dpsk_60ms.json"))
    mea_9 = mea_9_xor_dpsk_70ms.analyze.analyze(mea_9_xor_dpsk_70ms.analyze.readMeasurements("mea_9_xor_dpsk_70ms/220226_xor_dpsk_70ms.json"))

    ber = [
        [
            "10s",
            "20ms",
            "30ms",
            "40ms",
            "50ms",
            "60ms",
            "70ms",
            "100ms",
        ],
        [
            (mea_2["numPhasesErrors"] / mea_2["numPhasesDecoded"]) * 100,
            (mea_3["numPhasesErrors"] / mea_3["numPhasesDecoded"]) * 100,
            (mea_6["numPhasesErrors"] / mea_6["numPhasesDecoded"]) * 100,
            (mea_7["numPhasesErrors"] / mea_7["numPhasesDecoded"]) * 100,
            (mea_4["numPhasesErrors"] / mea_4["numPhasesDecoded"]) * 100,
            (mea_8["numPhasesErrors"] / mea_8["numPhasesDecoded"]) * 100,
            (mea_9["numPhasesErrors"] / mea_9["numPhasesDecoded"]) * 100,
            (mea_5["numPhasesErrors"] / mea_5["numPhasesDecoded"]) * 100,
        ]
    ]
    return ber

def plot():
    packetloss = getPacketLosses()
    ber = getBER()

    # Arrange plots
    fig, axs = plt.subplots(1,2)
    fig.suptitle("XOR DPSK")

    # Print barchart of BER
    axs[0].bar(range(len(ber[1])), ber[1])
    axs[0].set_xticks(range(len(ber[1])))
    axs[0].set_xticklabels(ber[0])
    axs[0].set_title("BER")
    axs[0].set_ylabel("percent [%]")

    # Print barchart of packetloss
    axs[1].bar(range(len(packetloss[1])), packetloss[1])
    axs[1].set_xticks(range(len(packetloss[1])))
    axs[1].set_xticklabels(packetloss[0])
    axs[1].set_title("Packetloss")
    axs[1].set_ylabel("percent [%]")

    plt.show()

def paperPlot():
    packetloss = getPacketLosses()
    ber = getBER()

    # Print barchart of BER
    plt.bar(range(len(ber[1])), ber[1])
    plt.xticks(range(len(ber[1])), ber[0])
#    plt.axes.Axes.set_xticklabels(ber[0])
    plt.title("Phase error")
    plt.ylabel("[%]")

    plt.show()

    # Print barchart of packetloss
    plt.bar(range(len(packetloss[1])), packetloss[1])
    plt.xticks(range(len(packetloss[1])),packetloss[0])
#  plt.axes.Axes.set_xticklabels(packetloss[0])
    plt.title("Packetloss")
    plt.ylabel("[%]")

    plt.show()


if __name__ == "__main__":
    plot()
