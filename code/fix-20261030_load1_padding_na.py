"""Write n/a for the unused second/third encoding slots of load-1 Sternberg trials (fix-20261030).

In the NWB trials table (DANDI 000673) a load-1 trial has one encoding picture; the columns of the 2nd and 3rd
picture hold 0 (PicIDs_Encoding2/3 = 0, timestamps_Encoding2/3 and *_end = 0.0). In this release 0 occurs in those
six columns in all 3003 load-1 trials and in no load-3 trial, so it marks an empty slot, not picture 0 or time 0 s.
This script replaces exactly those values by n/a in load-1 `sternberg_trial` rows; it asserts the pattern first.
Usage: python fix-20261030_load1_padding_na.py <bids_root>
"""
import csv, glob, json, os, sys

COLS = ["PicIDs_Encoding2", "PicIDs_Encoding3", "timestamps_Encoding2", "timestamps_Encoding2_end",
        "timestamps_Encoding3", "timestamps_Encoding3_end"]
NOTE = (" For load-1 trials the source stores 0 in this column (an unused slot); since 30 Oct 2026 it is written n/a "
        "(code/fix-20261030_load1_padding_na.py).")
root = sys.argv[1]
n = 0
for ev in sorted(glob.glob(os.path.join(root, "sub-*/ses-*/ieeg/*_task-sternberg_events.tsv"))):
    with open(ev, newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
        header = list(rows[0].keys())
    for r in rows:
        if r["trial_type"] != "sternberg_trial":
            continue
        if r["loads"] == "1":
            for c in COLS:
                assert float(r[c]) == 0, (ev, c, r[c])
                r[c] = "n/a"
            n += 1
        else:
            assert r["loads"] == "3" and all(float(r[c]) != 0 for c in COLS), (ev, r["loads"])
    with open(ev, "w", newline="") as f:
        w = csv.DictWriter(f, header, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    js = ev[:-4] + ".json"
    d = json.load(open(js))
    for c in COLS:
        if c in d and NOTE not in d[c].get("Description", ""):
            d[c]["Description"] = d[c].get("Description", "") + NOTE
    first = open(js).read().split("\n")[1]
    ind = len(first) - len(first.lstrip(" "))
    with open(js, "w") as f:
        json.dump(d, f, indent=ind, ensure_ascii=False)
        f.write("\n")
print("load-1 trials changed:", n)
