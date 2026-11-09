"""Hand calculation for the two-aircraft trail experiment (no BlueSky needed).

Gap change = closing speed x time. Calibrated airspeed (CAS) is converted to true airspeed (TAS) with the ISA density at the
flight altitude (low-speed approximation, no compressibility correction).
"""
from math import sqrt

ALT_FT = 5000.0
CAS_LEAD, CAS_FOLL = 130.0, 160.0      # kt
GAP0 = 8.0                             # NM at the start
T_END, T_INSTR = 6.0, 3.0              # minutes


def tas_over_cas(alt_ft):
    density_ratio = (1 - 6.8756e-6 * alt_ft) ** 4.2559     # ISA troposphere
    return 1 / sqrt(density_ratio)


k = tas_over_cas(ALT_FT)
v_lead, v_foll = CAS_LEAD * k, CAS_FOLL * k
closing = v_foll - v_lead

if __name__ == "__main__":
    print("TAS/CAS at %.0f ft: %.3f" % (ALT_FT, k))
    print("TAS leader %.1f kt, follower %.1f kt, closing speed %.1f kt" % (v_lead, v_foll, closing))
    print("Baseline gap at %.0f min: %.2f NM" % (T_END, GAP0 - closing * T_END / 60))
    print("Time to reach 5 NM without intervention: %.2f min" % ((GAP0 - 5.0) / closing * 60))
    print("Sequenced gap if the follower slowed instantly at minute %.0f: %.2f NM" % (T_INSTR, GAP0 - closing * T_INSTR / 60))
