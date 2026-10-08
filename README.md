[![DOI](https://img.shields.io/badge/DOI-10.82901%2Fnemar.nm000368-blue)](https://doi.org/10.82901/nemar.nm000368)

Sternberg working memory: human microwire LFP (Daume et al. 2024, DANDI 000673)
================================================================================

Overview
--------
Microwire local field potentials (LFP) from Behnke-Fried hybrid depth electrodes in patients with
drug-resistant epilepsy undergoing invasive seizure monitoring, recorded while they performed a Sternberg
working-memory task with pictures (load 1 or load 3, 140 trials per session). Recording sites:
hippocampus, amygdala, dorsal anterior cingulate cortex (dACC), pre-supplementary motor area (pre-SMA) and
ventromedial prefrontal cortex (vmPFC). The study was part of an NIH BRAIN consortium of Cedars-Sinai
Medical Center, Toronto Western Hospital and Johns Hopkins Hospital.

This dataset is an iEEG-BIDS representation of the LFP released by the authors in NWB format on DANDI:

  Daume J, Kaminski J, Schjetnan AGP, Salimpour Y, Khan U, Kyzar M, Reed CM, Anderson WS, Valiante TA,
  Mamelak AN, Rutishauser U (2025). Data for: Control of working memory by phase-amplitude coupling of
  human hippocampal neurons (Version 0.250122.0110). DANDI Archive.
  https://doi.org/10.48324/dandi.000673/0.250122.0110  (license CC-BY-4.0)

  Article: Daume J et al. Control of working memory by phase-amplitude coupling of human hippocampal
  neurons. Nature 629, 393-401 (2024). https://doi.org/10.1038/s41586-024-07309-z

Please cite both. Example analysis code: https://github.com/rutishauserlab/SBCAT-release-NWB.
Related release: DANDI 000469 (Kyzar et al., Sternberg task, single-neuron spike times only, no continuous
signal) comes from the same lab and task; its subject labels were not cross-checked here.
Same participants in other releases: the NWB file identifiers carry the lab patient code (e.g. P62CS, P101TWH,
P1802JHU; column lab_patient_code of participants.tsv; the suffix appears to name the site: CS Cedars-Sinai, TWH
Toronto Western, JHU Johns Hopkins). Where the same code appears in another public release with the same age and
sex, participants.tsv names that subject (column same_participant_in): 9 participants were also recorded in the
cognitive-boundary task of DANDI 000940 (Zheng et al. 2024; NEMAR nm000367) and 5 (P55CS, P56CS, P58CS, P60CS,
P62CS) in the movie-watching study DANDI 000623 (NEMAR nm000357). These are different tasks and recordings, not
duplicates. One code (P116TWH here, TWH116 in DANDI 000940) has a different age and sex in the two releases and is
not linked.

Ethics
------
From the article: "Their participation was voluntary, and all of the patients gave their informed consent.
This study was part of an NIH Brain consortium between three institutions (Cedars-Sinai Medical Center,
Toronto Western Hospital and Johns Hopkins Hospital) and was approved by the Institutional Review Board of
the institution at which the patient was enrolled." This deposit redistributes the publicly released data
under its CC-BY-4.0 license.

Contents
--------
35 participants, 43 recordings (sessions), 1,922 microwire LFP channels (8-71 per recording), 400 Hz,
1221-1899 s per recording, 17.23 h in total; 6,007 trial rows, 42,139 TTL markers, 24,028 picture presentations.

  sub-<label>/ses-<label>      DANDI subject and session labels (ses-1, ses-2, ses-3).
  ieeg/*_ieeg.vhdr/.vmrk/.eeg  BrainVision, IEEE float32, microvolts, resolution 1.0.
  ieeg/*_channels.tsv          one row per microwire, in the column order of the source series.
  ieeg/*_electrodes.tsv        source coordinates of each microwire (one location per bundle).
  ieeg/*_events.tsv            trials, TTL markers and picture presentations (see Events).
  *_scans.tsv                  recording year, source file, SHA-256 and float32 rounding error.
  sourcedata/sourcedata_provenance.json
                               the 44 source NWB files with size, SHA-256, DANDI asset id and download URL.

Why the original NWB files are not included: they embed the stimulus pictures (stimulus/templates,
StimulusTemplates, 400 x 300 RGB images). The article states "Due to copyright restrictions, the images
shown here are similar but not identical to those used in the study", so the pictures have their own
copyright. The NWB files (and the pictures) remain available unchanged from DANDI with the URLs and
checksums in sourcedata/sourcedata_provenance.json, e.g. `dandi download DANDI:000673/0.250122.0110`.

Signal: what was converted and how
----------------------------------
Source: acquisition/LFPs (ElectricalSeries) of each NWB file: float64 values in "microvolts", conversion 1,
offset 0, regular 400 Hz clock (starting_time between 0.0000153 and 0.0025 s in the session clock). NWB
description: "These are LFP recordings that have spike potentials removed and is downsampled to 400Hz".
Values were written to BrainVision as float32 microvolts; this is the only change (float32 rounding, at
most 0.00049 µV per file, reported per file in scans.tsv). No filtering, resampling, re-referencing,
cropping or channel removal was done by this conversion.

Processing already applied by the authors (Daume et al. 2024, Methods): broadband 0.1-8000 Hz recorded at
32 kHz (Neuralynx ATLAS; Cedars-Sinai and Toronto Western) or 30 kHz (Blackrock; Johns Hopkins); spike
waveforms removed by linear interpolation from -1 to 2 ms around each spike onset on all wires of the bundle;
zero phase-lag low-pass at 175 Hz; downsampling to 400 Hz. The article then removes 60/120 Hz line noise for
its analyses; whether that band-stop was applied to the released series is not stated. Reference: locally
within each bundle (one of the eight microwires or a dedicated low-impedance reference wire); the reference
wire per channel is not given. Channel type: BIDS has no microwire channel type; SEEG (depth electrode) is used
and each channel is described as a microwire in channels.tsv.
Institution: every NWB file states general/institution = "Cedars-Sinai Medical Center", although the article
reports recordings at three institutions; the release gives no explicit per-patient site. The
recording_institution column and InstitutionName repeat the NWB value; the lab patient code suffix (CS, TWH,
JHU) in participants.tsv suggests the site.

Events
------
onset = NWB time - LFP starting_time (all NWB times share the session clock). Because the LFP starts up to
2.5 ms after the session-clock zero, the experiment-start TTL can have a small negative onset.
  sternberg_trial        one row per trial (intervals/trials; onset = trial start, duration = stop - start),
                         with all source columns: loads, PicIDs_Encoding1/2/3, PicIDs_Probe, probe_in_out,
                         response_accuracy and the absolute NWB times timestamps_FixationCross,
                         timestamps_Encoding1/2/3(_end), timestamps_Maintenance, timestamps_Probe,
                         timestamps_Response.
  ttl                    every TTL marker (acquisition/events): 61 start of experiment, 11 fixation cross,
                         1/2/3 picture 1/2/3 shown, 5 transition between pictures, 6 end of encoding / start
                         of maintenance, 7 probe, 8 response, 60 end of experiment (NWB description).
  stimulus_presentation  every picture presentation (stimulus/presentation/StimulusPresentation, IndexSeries);
                         stimulus_index indexes the source StimulusTemplates (not distributed, see above).
NWB column descriptions are copied into events.json. Times inside source columns are absolute NWB session
times (subtract source_lfp_starting_time_s in scans.tsv to get recording time).

Coordinates
-----------
electrodes.tsv gives the x, y, z of the NWB electrodes table in mm (one location per bundle). The article
plots electrode positions "on the CITI168 Atlas Brain in MNI152 coordinates for the sole purpose of
visualization" and notes that template coordinates can fall into white matter; coordsystem.json therefore
uses "Other" with that description.

Participants
------------
Cohort (Daume et al. 2024, Methods and Supplementary Table S5): 36 patients (44 sessions; 21 female, 15 male;
age 40.47 +/- 13.76 years) with Behnke-Fried hybrid electrodes (AdTech) implanted for intracranial seizure
monitoring and evaluation for surgical treatment of drug-resistant epilepsy, at Cedars-Sinai Medical Center,
Toronto Western Hospital and Johns Hopkins Hospital. Recording years (NWB, year only): 2018-2022.
sub-20 (lab code P088TWH) is not included: its only NWB file has spike-sorted units but no LFP series
(acquisition/LFPs absent), so 35 of the 36 DANDI participants are present (Table S5: P88T, male, 26, right
mesial temporal onset).

participants.tsv columns:
  age, sex, species, recording_institution, dandi_subject_id   NWB general/subject and general/institution.
  lab_patient_code, same_participant_in                         NWB file identifier; links to other releases.
  seizure_onset_zone                                            Daume et al. 2024 Supplementary Table S5, verbatim.
  paper_session_labels, n_sessions                              Table S5 row labels of the participant's sessions
                                                                (first = ses-1, _2 = ses-2, _3 = ses-3).
  diagnosis, implant_type                                       cohort-level facts from the article Methods.
  recording_year                                                year of NWB session_start_time (as scans.tsv).
  lfp_regions, lfp_hemispheres                                  derived from channels.tsv of this release.
Mapping proof: Table S5 names rows by lab code (P55cs, P101T, P1802jh, ...). For all 35 participants the code,
age, sex and number of sessions agree, and for every one of the 43 sessions the number of LFP channels per area
(hippocampus, amygdala, pre-SMA, dACC, vmPFC) in this release equals Table S5's number of clean micro-LFP
channels per area. Table S5 also gives neuron counts per session and area (not copied here).
Handedness, epilepsy duration/onset age, etiology and medication are not reported by the sources (n/a).
Recording year (scans.tsv) is the year of the NWB session_start_time, which the authors set to 1 January of
the recording year to avoid disclosure of protected health information.

Not converted (available unchanged in the NWB files on DANDI)
--------------------------------------------------------------
Spike-sorted single units (spike times, waveforms and quality metrics) and the stimulus pictures.

Conversion checks
-----------------
- Every BrainVision file was read back with MNE-Python and compared with the source NWB: channel names and
  order equal the NWB electrode region, sampling rate and sample count equal, every sample equals the
  float32 representation of the source value (largest absolute difference to the float64 source
  0.00049 µV), no non-finite values.
- Every trial row, TTL marker and picture presentation was recomputed from the NWB (onset = time -
  starting_time); all match events.tsv within 1 µs; only the experiment-start TTL of each file lies
  before the first sample (by at most 2.5 ms).
- scans.tsv SHA-256 values equal the DANDI digests of the source files.
- bids-validator 3.0.2: 0 errors; warnings only for recommended fields the source does not document.

Conversion code: b2dandi_rutishauser_bids.py (iEEG-NEMAR campaign, batch 2), using h5py and pybv.

Known caveats
-------------
- Every NWB file states general/institution = "Cedars-Sinai Medical Center" although the article reports three
  sites; recording_institution and InstitutionName repeat the NWB value (see Signal).
- Whether the article's 60/120 Hz band-stop was applied to the released series is not stated; the reference
  wire per channel is not given (see Signal).
- The stimulus pictures are not distributed (copyright; see Contents).
- One code (P116TWH here, TWH116 in DANDI 000940) has a different age and sex in the two releases and is not
  linked; DANDI 000940 states 2018 for all its files, including patients whose Sternberg sessions here are dated
  2019 or 2020.

How to load
-----------
  from mne_bids import BIDSPath, read_raw_bids
  bp = BIDSPath(root="nm000368", subject="1", session="1", task="sternberg", datatype="ieeg")
  raw = read_raw_bids(bp)            # 400 Hz microwire LFP in microvolts (MNE stores volts)
  events = raw.annotations           # trials, TTL markers, picture presentations from events.tsv

Citation
--------
Daume J, Kaminski J, Schjetnan AGP, Salimpour Y, Khan U, Kyzar M, Reed CM, Anderson WS, Valiante TA, Mamelak AN,
Rutishauser U. Control of working memory by phase-amplitude coupling of human hippocampal neurons. Nature 629,
393-401 (2024). doi:10.1038/s41586-024-07309-z ; and the data: doi:10.48324/dandi.000673/0.250122.0110.

Provenance of the 2026-10-07 metadata enrichment
------------------------------------------------
Daume et al. 2024 Methods and Supplementary Information (Supplementary Table S5); the release itself
(channels.tsv, scans.tsv).
