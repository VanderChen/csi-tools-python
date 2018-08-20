import numpy as np
from signal_proc.bpsk import *

def get_simo_SNRs(csi):
    ret = np.sum(np.multiply(csi,np.conj(csi)))
    ret = ret.real
    return ret
    pass

def get_eff_SNRs(csi):
    et = np.zeros(7,4) + np.spacing(1)
    csi_size = csi.shape

    k = np.min(csi[1:])

    if k>=1:
        snrs = get_simo_SNRs(csi)

        bers = bpsk_ber(snrs)
        mean_ber = np.mean([np.mean(bers),2])
        
        pass
    pass

def get_eff_SNRs_sm(csi):
    ret = np.zeros(7,4) + np.spacing(1)
    csi_size = csi.shape

    k = np.min(csi[1:])

    if k >= 1:
        snrs = get_eff_SNRs_sm
    pass