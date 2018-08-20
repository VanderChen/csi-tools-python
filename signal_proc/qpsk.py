# -*- coding: UTF-8 -*-

# Quadrature Phase Shift Keyin

import numpy as np
from scipy.stats import norm

def qpsk_ber(snr):
    ret = norm.sf(np.sqrt(snr))
    return ret

def qpsk_berinv(ber):
    ret = np.square(norm.isf(ber))
    return ret