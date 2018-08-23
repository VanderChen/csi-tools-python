import numpy as np
from signal_proc.bpsk import *
import sys

def get_mimo3_SNRs(csi):
    return csi

def get_mimo3_SNRs_sm(csi):
    return csi

def mimo2_mmse(csi):
    M = np.linalg.inv(np.dot(np.conj(csi),np.transpose(csi)) + np.eye(2))
    ret = 1 / np.diag(M) - 1
    ret = np.real(ret)
    return ret

def get_mimo2_SNRs(csi):
    csi_size = csi.shape  # [S M N]
    m = 30
    if csi_size[1] < 2 or csi_size[2] < 2:
        sys.exit("CSI matrix must have at least 2 TX antennas and 2 RX antennas")
    csi = csi / np.sqrt(2)
    if csi_size[1] == 2:
        ret = np.zeros((csi_size[0],1,2))
        for i in range(csi_size[0]):
            ret[i][0] = mimo2_mmse(np.squeeze(csi[i][:][:]))
    return ret

def get_mimo2_SNRs_sm(csi):
    
    return csi

def get_simo_SNRs(csi):
    ret = np.multiply(csi,np.conj(csi))
    ret = np.sum(ret,axis=1)
    ret = np.sum(ret,axis=1,keepdims=True)
    ret = ret.real
    return ret

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