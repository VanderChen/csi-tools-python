# -*- coding: UTF-8 -*-
# Binary Phase Shift Keying
import numpy as np
from scipy.stats import norm


def bpsk_ber(snr):
    ret = norm.sf(np.sqrt(2 * snr))
    return ret


def bpsk_berinv(ber):
    ret = np.square(norm.isf(ber)) / 2
    return ret
