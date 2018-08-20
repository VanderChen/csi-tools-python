# -*- coding: UTF-8 -*-

# Quadrature Amplitude Modulation

import numpy as np
from scipy.stats import norm


def qam16_ber(snr):
    ret = 3/4 * norm.sf(np.sqrt(snr/5))
    return ret


def qam16_berinv(ber):
    ret = np.square(norm.isf(ber * 4/3)) * 5
    return ret


def qam64_ber(snr):
    ret = 7/12 * norm.sf(np.sqrt(snr/21))
    return ret


def qam64_berinv(ber):
    ret = np.square(norm.isf(ber * 12/7)) * 21
    return ret
