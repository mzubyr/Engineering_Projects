"""Separations from the positions printed by BlueSky (POS command, after the 6-minute stop), and a comparison with the hand calculation.

Run: python analyze_results.py     (writes results/summary.md)
"""
from separation import dms, separation_nm
import hand_calculation as hc

AIRPORT = (12.0476, 8.5247)            # Kano (approximate), only used for the distance to the airport

# Positions as printed by BlueSky (POS APK201, POS APK305) at the end of each run.
MEASURED = {
    "baseline":  {"APK201": ("N11'57'20.0", "E008'21'45.0"), "APK305": ("N11'54'56.0", "E008'17'31.0")},
    "sequenced": {"APK201": ("N11'57'20",   "E008'21'45"),   "APK305": ("N11'54'25",   "E008'16'36")},
}

lines = []
def log(s=""):
    print(s); lines.append(s)

pos = {run: {ac: (dms(la), dms(lo)) for ac, (la, lo) in d.items()} for run, d in MEASURED.items()}
sep = {run: separation_nm(*p["APK201"], *p["APK305"]) for run, p in pos.items()}
dist_ap = {run: separation_nm(*p["APK305"], *AIRPORT) for run, p in pos.items()}

log("| Run | Follower distance to airport (NM) | Separation at 6 min (NM) | Hand calculation (NM) |")
log("|---|---|---|---|")
log("| Baseline (no instruction) | %.1f | %.2f | %.2f |" % (dist_ap["baseline"], sep["baseline"], hc.GAP0 - hc.closing * hc.T_END / 60))
log("| Sequenced (speed instruction at minute 3) | %.1f | %.2f | %.2f (instant speed change) |"
    % (dist_ap["sequenced"], sep["sequenced"], hc.GAP0 - hc.closing * hc.T_INSTR / 60))

# Estimate of the deceleration time of the follower.
# Distance not flown in the sequenced run (compared with the baseline) = dV * (T_after - T_dec / 2) / 60,
# where dV is the speed reduction (TAS), T_after = minutes from the instruction to the stop, T_dec = deceleration time (minutes).
not_flown = separation_nm(*pos["baseline"]["APK305"], *pos["sequenced"]["APK305"])
dv = hc.v_foll - hc.v_lead
t_after = hc.T_END - hc.T_INSTR
t_dec = 2 * (t_after - not_flown * 60 / dv)
log("")
log("The follower flew %.2f NM less in the sequenced run." % not_flown)
log("Estimated deceleration time from 160 to 130 kt (a rough estimate that assumes a constant deceleration): %.1f min (about %.0f s)." % (t_dec, t_dec * 60))
log("BlueSky's own deceleration model has not been checked.")
open("results/summary.md", "w").write("\n".join(lines) + "\n")
