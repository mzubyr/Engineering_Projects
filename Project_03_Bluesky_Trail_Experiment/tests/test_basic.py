import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from separation import dms, separation_nm
import hand_calculation as hc


def test_dms_conversion():
    assert abs(dms("N11'57'20.0") - 11.955556) < 1e-5
    assert abs(dms("E008'21'45") - 8.3625) < 1e-6
    assert dms("S10'30'0") < 0


def test_one_degree_of_latitude_is_about_60_nm():
    assert abs(separation_nm(0, 0, 1, 0) - 60.0) < 0.2


def test_start_gap_is_8_nm():
    assert abs(separation_nm(11.8392, 8.1563, 11.7724, 8.0385) - 8.0) < 0.05


def test_hand_calculation():
    assert abs(hc.k - 1.077) < 0.001
    assert abs((hc.GAP0 - hc.closing * 6 / 60) - 4.77) < 0.02
    assert abs((hc.GAP0 - hc.closing * 3 / 60) - 6.38) < 0.02
