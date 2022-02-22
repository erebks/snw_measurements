import json
import sys

if (len(sys.argv) < 3):
    print("Too less arguments!")
    print("Use: python3 {0} in_file out_file".format(sys.argv[0]))
    exit(1)

in_file = open(sys.argv[1], "r")

try:
    out_file = open(sys.argv[2], "r")
    o_json = json.loads(out_file.read())
    out_file.close()
except OSError as e:
    o_json = []

# Read all json nodes in out_file

def readjson(f):
    j = []
    try:
        s = f.readlines()
    except:
        return []

    for line in s:
        if line == '\n':
            continue
        else:
            j.append(json.loads(line))

    return j

i_json = readjson(in_file)

in_file.close()

# Extract only "received_at" timestamps of both
ij_timestamps = []
for ij in i_json:
    ij_timestamps.append(ij["result"]["received_at"])

oj_timestamps = []
for oj in o_json:
    oj_timestamps.append(oj["result"]["received_at"])

for ij_ts in ij_timestamps:
    if not ij_ts in oj_timestamps:
        # Find ij entry
        ij_found = None
        for ij in i_json:
            if ij["result"]["received_at"] == ij_ts:
                ij_found = ij
                break
        # Add to list
        print("Adding: {0}".format(ij_found))
        o_json.append(ij_found)
    else:
        print("Ignoring: {0}".format(ij_ts))

out_file = open(sys.argv[2], "w")
out_file.write(json.dumps(o_json))
out_file.close()
