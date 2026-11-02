"""Receipt for the stimulus_presentation rows with stimulus_index 0.

usage: python 2026-11-02_stimulus-index-zero.py BIDS_ROOT DANDI_000673_ROOT

BIDS_ROOT is a checkout of nm000368; DANDI_000673_ROOT holds the source NWB files
in the DANDI layout of sourcedata/sourcedata_provenance.json. Prints markdown.
"""

import argparse
import hashlib
import json
import pathlib

import h5py
import numpy as np
import pandas as pd

TOL = 1e-6  # s, onset rounding in events.tsv


def git_blob(path: pathlib.Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 24):
            h.update(chunk)
    return h.hexdigest()


def nwb_stats(path: pathlib.Path) -> dict:
    with h5py.File(path, "r") as f:
        refs = f["stimulus/templates/StimulusTemplates/order_of_images"][:]
        series = f["stimulus/presentation/StimulusPresentation"]
        index = series["data"][:]
        times = series["timestamps"][:]
        template0 = f[refs[0]].name.rsplit("/", 1)[-1]
    zero = np.flatnonzero(index == 0)
    last_picture = np.maximum.accumulate(np.where(index != 0, np.arange(len(index)), -1))
    offsets_ms = (times[zero] - times[last_picture[zero]]) * 1e3
    deviation_us = np.abs(offsets_ms - np.where(offsets_ms < 15, 10, 20)).max(initial=0) * 1e3
    return {"template0": template0, "n_zero": len(zero), "deviation_us": deviation_us}


def bids_stats(path: pathlib.Path) -> dict:
    ev = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)
    onset = ev.onset.astype(float)
    trials = ev[ev.trial_type == "sternberg_trial"]
    stim = ev[ev.trial_type == "stimulus_presentation"]
    zero = stim[stim.stimulus_index == "0"]
    ttl = ev[ev.trial_type == "ttl"]
    picids = ev.filter(like="PicIDs_")
    out = {
        "load1": int((trials.loads == "1").sum()),
        "load3": int((trials.loads == "3").sum()),
        "stim": len(stim),
        "zero": len(zero),
        "exactly2": 0,
        "offsets_ms": set(),
        "in_picture1": 0,
        "zero_in_load1": 0,
        "from_start_s": [],
        "ttl_at_zero": sum(
            int(((onset[ttl.index] - t).abs() < 5e-4).sum()) for t in onset[zero.index]
        ),
        "ttl23_load1": 0,
        "picid_999": int(picids.isin(["999", "999.0"]).sum().sum()),
    }
    for _, trial in trials[trials.loads == "1"].iterrows():
        start = float(trial.onset)
        inside = (onset >= start - TOL) & (onset <= start + float(trial.duration) + TOL)
        rows = stim[inside[stim.index]]
        z = rows[rows.stimulus_index == "0"]
        picture1 = float(rows[rows.stimulus_index != "0"].onset.iloc[0])
        out["exactly2"] += len(z) == 2
        out["zero_in_load1"] += len(z)
        out["ttl23_load1"] += int(ttl[inside[ttl.index]].value.isin(["2", "3"]).sum())
        enc1, enc1_end = float(trial.timestamps_Encoding1), float(trial.timestamps_Encoding1_end)
        for _, row in z.iterrows():
            out["offsets_ms"].add(round((float(row.onset) - picture1) * 1e3, 2))
            out["from_start_s"].append(float(row.onset) - start)
            out["in_picture1"] += enc1 - TOL <= float(row.source_start_time) <= enc1_end + TOL
    out["blob"] = git_blob(path)[:10]
    return out


def session_key(entry: dict) -> tuple[int, ...]:
    sub, ses = pathlib.Path(entry["file"]).stem.split("_")[:2]
    return int(sub.removeprefix("sub-")), int(ses.removeprefix("ses-"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bids_root", type=pathlib.Path)
    parser.add_argument("dandi_root", type=pathlib.Path)
    args = parser.parse_args()
    provenance = json.loads((args.bids_root / "sourcedata/sourcedata_provenance.json").read_text())
    header = (
        "session | events.tsv blob | load-1 / load-3 trials | stimulus rows | index-0 rows"
        " | load-1 trials with exactly 2 | offsets after picture 1 (ms) | in picture-1 interval"
        " | index-0 outside load-1 trials | TTL within 0.5 ms | TTL 2/3 in load-1 trials"
        " | NWB sha256 = provenance | NWB index-0 entries | NWB template 0"
    )
    print("| " + header + " |")
    print("|" + "---|" * (header.count("|") + 1))
    totals: dict = {"sessions": 0, "load1": 0, "zero": 0, "stim": 0, "from_start_s": [], "dev": 0.0}
    for entry in sorted(provenance["files"], key=session_key):
        nwb = nwb_stats(args.dandi_root / entry["file"])
        sha_ok = "yes" if sha256(args.dandi_root / entry["file"]) == entry["sha256"] else "NO"
        sub, ses = pathlib.Path(entry["file"]).stem.split("_")[:2]
        events = args.bids_root / sub / ses / "ieeg" / f"{sub}_{ses}_task-sternberg_events.tsv"
        nwb_cols = f"{sha_ok} | {nwb['n_zero']} | {nwb['template0']}"
        totals["dev"] = max(totals["dev"], nwb["deviation_us"])
        if not events.exists():
            print(
                f"| {sub} {ses} | not in this release | "
                + " | ".join(["-"] * 9)
                + f" | {nwb_cols} |"
            )
            continue
        b = bids_stats(events)
        totals["sessions"] += 1
        for key in ("load1", "zero", "stim"):
            totals[key] += b[key]
        totals["from_start_s"] += b["from_start_s"]
        offsets = ", ".join(f"{o:.2f}" for o in sorted(b["offsets_ms"]))
        print(
            f"| {sub} {ses} | {b['blob']} | {b['load1']} / {b['load3']} | {b['stim']} | {b['zero']}"
            f" | {b['exactly2']} | {offsets} | {b['in_picture1']} | {b['zero'] - b['zero_in_load1']}"
            f" | {b['ttl_at_zero']} | {b['ttl23_load1']} | {nwb_cols} |"
        )
        assert b["picid_999"] == 0, f"{events.name}: PicIDs value 999 found"
    starts = totals["from_start_s"]
    print()
    print(
        f"Totals: {totals['sessions']} sessions, {totals['load1']} load-1 trials,"
        f" {totals['zero']} index-0 rows of {totals['stim']} stimulus rows;"
        f" index-0 rows {min(starts):.2f}-{max(starts):.2f} s after trial start;"
        f" NWB offsets within {totals['dev']:.1g} us of 10/20 ms; no PicIDs value 999."
    )


if __name__ == "__main__":
    main()
