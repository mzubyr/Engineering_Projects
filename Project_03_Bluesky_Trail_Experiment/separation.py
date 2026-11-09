"""Distance between two positions given as BlueSky prints them (degrees, minutes, seconds) or in decimal degrees."""
import re
from math import radians, sin, cos, asin, sqrt

R_NM = 3440.065   # mean Earth radius in nautical miles


def dms(text):
    """'N11\\'57\\'20.0' -> 11.9556 ;  'E008\\'21\\'45' -> 8.3625 (S and W give negative values)."""
    m = re.match(r"\s*([NSEW])\s*(\d+)['\u2019\u00b0]\s*(\d+)['\u2019]\s*([\d.]+)", text)
    if not m:
        raise ValueError("cannot read position: %r" % text)
    hemi, d, mi, s = m.group(1), int(m.group(2)), int(m.group(3)), float(m.group(4))
    value = d + mi / 60 + s / 3600
    return -value if hemi in "SW" else value


def separation_nm(lat1, lon1, lat2, lon2):
    """Great-circle distance in nautical miles (haversine formula)."""
    la1, lo1, la2, lo2 = map(radians, (lat1, lon1, lat2, lon2))
    h = sin((la2 - la1) / 2) ** 2 + cos(la1) * cos(la2) * sin((lo2 - lo1) / 2) ** 2
    return 2 * R_NM * asin(sqrt(h))
