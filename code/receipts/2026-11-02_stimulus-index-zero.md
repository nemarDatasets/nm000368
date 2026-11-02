# Receipt: stimulus_presentation rows with stimulus_index 0

**Claim**: the 6,006 stimulus_presentation rows with stimulus_index 0 are the two unused picture slots of each
load-1 trial (template image_999), exactly 2 per load-1 trial in all 43 sessions, 10 ms and 20 ms after the
trial's picture-1 row; no events rows are changed.

**Source**
- NEMAR events.tsv of all 43 sessions, read from a checkout of this PR branch. This PR does not change them:
  they equal main `d3d84340354e5360c4eea98b4e521905956f4066` (git blob ids in the table; compare with
  `git ls-tree -r HEAD`).
- The 44 source NWB files of DANDI 000673 version 0.250122.0110, identified by SHA-256 against
  `sourcedata/sourcedata_provenance.json` (44 of 44 equal).

**Method** (`2026-11-02_stimulus-index-zero.py BIDS_ROOT DANDI_000673_ROOT`; Python 3.12, pandas 3.1.0,
numpy 2.5.4, h5py 3.16.0; events.tsv read as text)
- Trial window: `onset` to `onset + duration` of each sternberg_trial row (1 µs tolerance). Rows inside the
  window of a load-1 trial (`loads` = 1) belong to it.
- Per load-1 trial: number of stimulus_index 0 rows; their offset from the trial's first stimulus_presentation
  row with a non-zero index (picture 1), rounded to 0.01 ms; whether their `source_start_time` lies between the
  trial's `timestamps_Encoding1` and `timestamps_Encoding1_end`; TTL markers with value 2 or 3 in the window.
- Per session: stimulus_index 0 rows outside load-1 trials; TTL markers within 0.5 ms of a stimulus_index 0 row;
  PicIDs_* values equal to 999 (the script stops if any).
- NWB: name of entry 0 of `stimulus/templates/StimulusTemplates/order_of_images`; number of 0 entries in
  `stimulus/presentation/StimulusPresentation/data`; offset of each 0 entry from the last non-zero entry before
  it, from the float64 `timestamps`. No signal or image values are used or reported (SHA-256 hashes whole files).

**Result**

| session | events.tsv blob | load-1 / load-3 trials | stimulus rows | index-0 rows | load-1 trials with exactly 2 | offsets after picture 1 (ms) | in picture-1 interval | index-0 outside load-1 trials | TTL within 0.5 ms | TTL 2/3 in load-1 trials | NWB sha256 = provenance | NWB index-0 entries | NWB template 0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sub-1 ses-1 | 93ace1e695 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-1 ses-2 | 7f42cb4ccc | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-2 ses-1 | f1a19a42e1 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-3 ses-1 | fe042b61f3 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-4 ses-1 | 644908b3d4 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-5 ses-1 | 0151df45db | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-5 ses-2 | bf98285678 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-6 ses-1 | e2819ee6e9 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-7 ses-1 | c88e54e85c | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-8 ses-1 | 6057391d9e | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-9 ses-1 | 6070ec5b35 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-10 ses-1 | b947f16fac | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-11 ses-1 | bfa3488e2e | 70 / 69 | 556 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-12 ses-1 | a96baab54f | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-12 ses-2 | 7e19af9331 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-13 ses-1 | e0cf3c7d0b | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-14 ses-1 | 54402d6d88 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-15 ses-1 | 0a4643fcea | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-16 ses-1 | cb0fe8cd01 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-17 ses-1 | 65aa011767 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-18 ses-1 | 610b1bcdb6 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-19 ses-1 | d7d7f6c3be | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-19 ses-2 | 1ad2d83288 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-20 ses-1 | not in this release | - | - | - | - | - | - | - | - | - | yes | 140 | image_999 |
| sub-21 ses-1 | 79808fe9b5 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-22 ses-1 | ee6e0b0a71 | 63 / 65 | 512 | 126 | 63 | 10.00, 20.00 | 126 | 0 | 0 | 0 | yes | 126 | image_999 |
| sub-22 ses-2 | c7d2ebf8a5 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-22 ses-3 | 444c7432b8 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-23 ses-1 | d4453b785a | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-24 ses-1 | 1373c6d1ec | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-25 ses-1 | da4a1b2cec | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-26 ses-1 | 033e184782 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-26 ses-2 | a7f1e1f4a1 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-27 ses-1 | cc910b63c2 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-28 ses-1 | 9cb7e4cb72 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-29 ses-1 | 2abee516ab | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-30 ses-1 | 4198d6d044 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-31 ses-1 | 2dc425c3cb | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-31 ses-2 | 160ab2c258 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-32 ses-1 | 5163be369b | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-33 ses-1 | 06d09e24f3 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-34 ses-1 | 25b866084a | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-35 ses-1 | 5ebff7be16 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |
| sub-36 ses-1 | 6c830b0906 | 70 / 70 | 560 | 140 | 70 | 10.00, 20.00 | 140 | 0 | 0 | 0 | yes | 140 | image_999 |

Totals: 43 sessions, 3003 load-1 trials, 6006 index-0 rows of 24028 stimulus rows; index-0 rows 0.93-1.38 s after trial start; NWB offsets within 2e-08 us of 10/20 ms; no PicIDs value 999.

sub-20 has no LFP series and is not in this release; its NWB file is listed for the template check only.

**Coverage**: 43 of 43 sessions (all events.tsv) and 44 of 44 source NWB files.
