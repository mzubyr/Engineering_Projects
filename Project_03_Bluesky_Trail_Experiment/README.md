# BlueSky experiment: two aircraft types in trail on final approach (Kano)

A small experiment in the open-source air traffic simulator BlueSky (TU Delft). Two aircraft of different types fly in trail on the same
final-approach track at Kano with a 30 kt speed difference. Question: **how fast does the separation erode, and what does a speed instruction do to it?**
It is a simulation of a simplified situation (see the limitations) and my BlueSky experience is basic.

## Set-up

- Track 060 (runway 06 extended centreline at Kano, airport position about 12.05 N, 8.52 E, approximate and for simulation only), level at 5000 ft, no wind.
- **Leader** `APK201`: Embraer 145 (`E145`), 130 kt CAS, starts 25 NM from the airport.
- **Follower** `APK305`: Boeing 737-800 (`B738`), 160 kt CAS, starts 8 NM behind the leader.
- `scenarios/baseline.scn`: no instruction. `scenarios/sequenced.scn`: the follower is told to slow to 130 kt at minute 3. Both runs stop at 6 minutes.
- The callsigns are invented for the simulation.

## How to run it in BlueSky

1. Install BlueSky (`pip install "bluesky-simulator[full]"`, in a Python environment that BlueSky supports) and start it with `bluesky`.
2. Find the scenario folder: in the BlueSky console type `CRE TEST A320 52.38 4.10 180 3000 150` and `SAVEIC FOLDERTEST`, then look for `FOLDERTEST.scn` on your disk.
3. Copy the two `.scn` files from `scenarios/` into that folder.
4. In the console: `RESET`, `IC BASELINE`; when it stops at 6 minutes, `POS APK201` and `POS APK305`. Then `RESET`, `IC SEQUENCED` and the same two `POS` commands.
5. Enter the printed positions in `analyze_results.py` and run it.

BlueSky version used: *(record the output of `pip show bluesky-simulator` here)*.

## Results

| Run | Follower distance to airport (NM) | Separation at 6 min (NM) | Hand calculation (NM) |
|---|---|---|---|
| Baseline (no instruction) | 15.8 | **4.79** (below 5 NM) | 4.77 |
| Sequenced (speed instruction at minute 3) | 16.8 | **5.83** | 6.38 (instant speed change assumed) |

Separations are computed from the latitude and longitude printed by BlueSky (rounded to one arc-second, about 0.03 NM) with the haversine formula.

**Hand calculation** (`hand_calculation.py`): gap change = closing speed x time. At 5000 ft the true airspeed is about 7.7 % above the calibrated speed (140 kt and 172 kt),
so the follower closes at about 32 kt, and an 8 NM gap falls below 5 NM after about 5.6 minutes.

## What it shows

- Without intervention, the 30 kt difference reduced the 8 NM gap to 4.8 NM in six minutes, as expected.
- The instruction kept the separation above 5 NM, but the result (5.8 NM) is lower than the 6.4 NM of the instant-change calculation. The follower flew 1.04 NM less than in
  the baseline, which suggests that it took roughly two minutes to slow from 160 to 130 kt (a rough estimate from the positions, assuming a constant deceleration; BlueSky's
  deceleration model has not been checked). Until the speeds matched, the gap kept shrinking.
- A speed instruction has to be given early, and the time it needs depends on the aircraft type. For a mixed fleet with very different performance, the time and distance
  needed for such corrections differ by type, which affects safety, capacity and controller workload.

## Files

| File | Purpose |
|---|---|
| `scenarios/` | The two BlueSky scenario files |
| `separation.py` | Position parsing (degrees, minutes, seconds) and great-circle distance |
| `hand_calculation.py` | Expected separations from the speed difference |
| `analyze_results.py` | Separations from the measured positions, comparison, deceleration-time estimate; writes `results/summary.md` |
| `tests/` | Automatic checks of the helper functions and the hand calculation |
| `docs/BlueSky_Experiment_Note.pdf` | One-page summary |

```
python hand_calculation.py
python analyze_results.py
python -m pytest tests        # optional (pip install pytest)
```

These scripts use only the Python standard library.

## Limitations

- Level flight, constant tracks, no wind, no descent profile, no wake-turbulence minima.
- Two aircraft only, and one run per case (BlueSky is deterministic here, but I did not repeat the runs).
- The deceleration time is an estimate from the final positions, not read from BlueSky's performance model.
- The airport position and the runway direction are approximate.

## Next steps

- Log positions automatically and compute the separation over time.
- Vary the speed difference, the instruction time and the aircraft types; add a descent profile and wake separation.
- Define metrics (minimum separation, time to loss of separation, number of instructions, runway throughput) over many scenarios.

## Author

Muhammad Ibrahim Zubair, Kano, Nigeria.
