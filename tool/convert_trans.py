import sys
import re
import struct

if len(sys.argv) != 3:
    print("Usage: python3 {}: <id2pdf-text> <trans-model-bin>".format(sys.argv[0]))
    print("Convert Kaldi transition model to pocketkaldi format.")
    print("    id2pdf-text: the transition-id to pdf map in transition model (generated by extract_id2pdf).")
    sys.exit(1)

from_file = sys.argv[1]
to_file = sys.argv[2]


with open(from_file) as fd:
    lines = list(map(lambda l: l.strip(), fd))
num_pdfs = int(lines[0])
num_transitions = int(lines[1])

map_list = [0 for i in range(num_transitions + 1)]
for line in lines[2: ]:
    tid, pdf = line.split()
    map_list[int(tid)] = int(pdf)

with open(to_file, 'wb') as fd:
    # VEC section: stats_sum
    fd.write(b"VEC0")
    fd.write(struct.pack("<i", len(map_list) * 4 + 4))
    fd.write(struct.pack("<i", len(map_list)))
    for v in map_list:
        fd.write(struct.pack("<i", v))
