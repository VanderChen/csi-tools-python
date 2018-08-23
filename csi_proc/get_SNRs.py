import numpy as np
from signal_proc.bpsk import *
from signal_proc.qpsk import *
from signal_proc.qam import *
import sys
from math import pi,exp

class SmMatrices:
    def __init__(self):
        self.SM_1 = 1
        self.SM_2_20 = [[1 , 1] , [1 , -1]] / np.sqrt(2)
        self.SM_2_40 = [[1 , 1j] , [1j , 1]] / np.sqrt(2)
        self.SM_3_20 = [[-2*pi/16 , -2*pi/(80/33) , 2*pi/(80/3)],[2*pi/(80/23) , 2*pi/(48/13) , 2*pi/(240/13)],[-2*pi/(80/13) , 2*pi/(240/37) , 2*pi/(48/13)]]
        self.SM_3_20 = np.power(exp(1),(np.multiply([1j] , self.SM_3_20))).tolist() / np.sqrt(3)
        self.SM_3_40 = [[-2*pi/16 , -2*pi/(80/13) , 2*pi/(80/23)],[-2*pi/(80/37) , -2*pi/(48/11) , -2*pi/(240/107)],[2*pi/(80/7) , -2*pi/(240/83) , -2*pi/(48/11)]]
        self.SM_3_40 = np.power(exp(1),(np.multiply([1j] , self.SM_3_40))).tolist() / np.sqrt(3)

def dbinv(x):
    ret = pow(10,(x/10))
    return ret

def apply_sm(csi,sm):
    csi_size = csi.shape
    if csi_size[1] == 1:
        ret = csi
    if len(csi_size) == 2:
        ret = np.zeros(csi_size)
        t = np.squeeze(csi)
        ret = np.transpose(np.dot(np.transpose(t) , sm))
    else:
        ret = np.zeros(csi_size)
        for i in range(csi_size[0]):
            t = np.squeeze(csi[i])
            ret[i] = np.transpose(np.dot(np.transpose(t) , sm))        
    return ret

def mimo3_mmse(csi):
    M = np.linalg.inv(np.dot(np.conj(csi),np.transpose(csi)) + np.eye(3))
    ret = 1 / np.diag(M) - 1
    ret = np.real(ret)
    return ret

def get_mimo3_SNRs(csi):
    csi_size = csi.shape  # [S M N]
    if csi_size[1] < 3 or csi_size[2] < 3:
        sys.exit("CSI matrix must have at least 3 TX antennas and 3 RX antennas")
    csi = csi / np.sqrt(dbinv(4.5))

    ret = np.zeros((csi_size[0],1,3))
    for i in range(csi_size[0]):
        ret[i][0] = mimo3_mmse(np.squeeze(csi[i]))
    return ret

def mimo3_mmse_sm(csi_i):
    const_sm = SmMatrices()
    csi = apply_sm(csi_i,const_sm.SM_3_20)
    M = np.linalg.inv(np.dot(np.conj(csi),np.transpose(csi)) + np.eye(3))
    ret = 1 / np.diag(M) - 1
    ret = np.real(ret)
    return ret

def get_mimo3_SNRs_sm(csi):
    csi_size = csi.shape  # [S M N]
    if csi_size[1] < 3 or csi_size[2] < 3:
        sys.exit("CSI matrix must have at least 3 TX antennas and 3 RX antennas")
    csi = csi / np.sqrt(dbinv(4.5))

    ret = np.zeros((csi_size[0],1,3))
    for i in range(csi_size[0]):
        ret[i][0] = mimo3_mmse_sm(np.squeeze(csi[i]))
    return ret

def mimo2_mmse(csi):
    M = np.linalg.inv(np.dot(np.conj(csi),np.transpose(csi)) + np.eye(2))
    ret = 1 / np.diag(M) - 1
    ret = np.real(ret)
    return ret

def get_mimo2_SNRs(csi):
    csi_size = csi.shape  # [S M N]
    if csi_size[1] < 2 or csi_size[2] < 2:
        sys.exit("CSI matrix must have at least 2 TX antennas and 2 RX antennas")
    csi = csi / np.sqrt(2)
    if csi_size[1] == 2:
        ret = np.zeros((csi_size[0],1,2))
        for i in range(csi_size[0]):
            ret[i][0] = mimo2_mmse(np.squeeze(csi[i]))
    else:
        ret = np.zeros((csi_size[0],3,2))
        for i in range(csi_size[0]):
            ret[i][0] = mimo2_mmse(np.squeeze(csi[i][[0,1]]))
            ret[i][1] = mimo2_mmse(np.squeeze(csi[i][[0,2]]))
            ret[i][2] = mimo2_mmse(np.squeeze(csi[i][[1,2]]))
    return ret

def mimo2_mmse_sm(csi_i):
    const_sm = SmMatrices()
    csi = apply_sm(csi_i,const_sm.SM_2_20)
    M = np.linalg.inv(np.dot(np.conj(csi),np.transpose(csi)) + np.eye(2))
    ret = 1 / np.diag(M) - 1
    ret = np.real(ret)
    return ret

def get_mimo2_SNRs_sm(csi):
    csi_size = csi.shape  # [S M N]
    if csi_size[1] < 2 or csi_size[2] < 2:
        sys.exit("CSI matrix must have at least 2 TX antennas and 2 RX antennas")
    csi = csi / np.sqrt(2)
    if csi_size[1] == 2:
        ret = np.zeros((csi_size[0],1,2))
        for i in range(csi_size[0]):
            ret[i][0] = mimo2_mmse_sm(np.squeeze(csi[i]))
    else:
        ret = np.zeros((csi_size[0],3,2))
        for i in range(csi_size[0]):
            ret[i][0] = mimo2_mmse_sm(np.squeeze(csi[i][[0,1]]))
            ret[i][1] = mimo2_mmse_sm(np.squeeze(csi[i][[0,2]]))
            ret[i][2] = mimo2_mmse_sm(np.squeeze(csi[i][[1,2]]))
    return ret

def get_simo_SNRs(csi):
    ret = []
    for i in np.multiply(csi,np.conj(csi)):
        ret.append(np.sum(i,axis=1,keepdims=2))
    ret = np.real(ret)
    return ret

def get_eff_SNRs(csi):
    ret = np.zeros((7,4)) + np.spacing(1)
    csi_size = csi.shape

    k = np.min(csi_size[1:])
    if k>=1:
        snrs = get_simo_SNRs(csi)

        bers = bpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0:len(mean_ber),0] = bpsk_berinv(mean_ber)

        bers = qpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0:len(mean_ber),1] = qpsk_berinv(mean_ber)

        bers = qam16_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0:len(mean_ber),2] = qam16_berinv(mean_ber)

        bers = qam64_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0:len(mean_ber),3] = qam64_berinv(mean_ber)

    
    if k >= 2:
        snrs = get_mimo2_SNRs(csi)

        bers = bpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 3:len(mean_ber) + 3,0] = bpsk_berinv(mean_ber)

        bers = qpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 3:len(mean_ber) + 3,1] = qpsk_berinv(mean_ber)

        bers = qam16_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 3:len(mean_ber) + 3,2] = qam16_berinv(mean_ber)

        bers = qam64_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 3:len(mean_ber) + 3,3] = qam64_berinv(mean_ber)


    if k >= 3:
        snrs = get_mimo3_SNRs(csi)

        bers = bpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 6:len(mean_ber) + 6,0] = bpsk_berinv(mean_ber)

        bers = qpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 6:len(mean_ber) + 6,1] = qpsk_berinv(mean_ber)

        bers = qam16_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 6:len(mean_ber) + 6,2] = qam16_berinv(mean_ber)

        bers = qam64_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 6:len(mean_ber) + 6,3] = qam64_berinv(mean_ber)

    return ret

def get_eff_SNRs_sm(csi):
    ret = np.zeros((7,4)) + np.spacing(1)
    csi_size = csi.shape

    k = np.min(csi_size[1:])
    if k>=1:
        snrs = get_simo_SNRs(csi)

        bers = bpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0:len(mean_ber),0] = bpsk_berinv(mean_ber)

        bers = qpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0:len(mean_ber),1] = qpsk_berinv(mean_ber)

        bers = qam16_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0:len(mean_ber),2] = qam16_berinv(mean_ber)

        bers = qam64_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0:len(mean_ber),3] = qam64_berinv(mean_ber)

    
    if k >= 2:
        snrs = get_mimo2_SNRs_sm(csi)

        bers = bpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 3:len(mean_ber) + 3,0] = bpsk_berinv(mean_ber)

        bers = qpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 3:len(mean_ber) + 3,1] = qpsk_berinv(mean_ber)

        bers = qam16_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 3:len(mean_ber) + 3,2] = qam16_berinv(mean_ber)

        bers = qam64_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 3:len(mean_ber) + 3,3] = qam64_berinv(mean_ber)


    if k >= 3:
        snrs = get_mimo3_SNRs_sm(csi)

        bers = bpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 6:len(mean_ber) + 6,0] = bpsk_berinv(mean_ber)

        bers = qpsk_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 6:len(mean_ber) + 6,1] = qpsk_berinv(mean_ber)

        bers = qam16_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 6:len(mean_ber) + 6,2] = qam16_berinv(mean_ber)

        bers = qam64_ber(snrs)
        mean_ber = np.mean(np.mean(bers,axis=0),axis=1)
        ret[0 + 6:len(mean_ber) + 6,3] = qam64_berinv(mean_ber)

    return ret