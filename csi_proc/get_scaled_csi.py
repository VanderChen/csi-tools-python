import numpy as np
from math import log10,pi,exp

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
    ret = pow(10,( x / 10))
    return ret

def db(x):
    ret = 10 * log10(x) + 300 -300
    return ret

def get_total_rss(csi_st):
    rssi_mag = 0
    if int(csi_st.rssi_a) != 0:
        rssi_mag = rssi_mag + dbinv(int(csi_st.rssi_a))
    if int(csi_st.rssi_b) != 0:
        rssi_mag = rssi_mag + dbinv(int(csi_st.rssi_b))
    if int(csi_st.rssi_c) != 0:
        rssi_mag = rssi_mag + dbinv(int(csi_st.rssi_c))  
    print(rssi_mag)
    ret = db(rssi_mag) - 44 - csi_st.agc
    return ret

def remove_sm(csi, rate):
    csi_size = csi.shape
    if csi_size[1] == 1:
        ret = csi

    ret = np.zeros(csi_size)
    ret_real = np.zeros(csi_size)
    ret_i = np.zeros(csi_size)
    const_sm = SmMatrices()
    if (rate & 2048) == 2048:
        if csi_size[1] == 3:
            sm = const_sm.SM_3_40
        elif csi_size[1] == 2:
            sm = const_sm.SM_2_40
    else:
        if csi_size[1] == 3:
            sm = const_sm.SM_3_20
        elif csi_size[1] == 2:
            sm = const_sm.SM_2_20
    for i in range(csi_size[0]):
        t = np.squeeze(csi[i])
        H = np.dot(np.transpose(t),np.conj(np.transpose(sm)))
        ret_real[i] = np.transpose(np.real(H))
        ret_i[i] = np.transpose(np.imag(H))
    ret = ret_real + np.multiply([1j] , ret_i)
    return ret
    
def get_scaled_csi(csi_st):
    csi = csi_st.csi

    csi_sq = np.multiply(csi,np.conj(csi))
    csi_pwr = np.sum(csi_sq)
    rssi_pwr = dbinv(get_total_rss(csi_st))
    scale = rssi_pwr / (csi_pwr / 30)
    if csi_st.noise == -127:
        noise_db = -92
    else:
        noise_db = csi_st.noise
    thermal_noise_pwr = dbinv(noise_db)
    quant_error_pwr = scale * (csi_st.Nrx * csi_st.Ntx)
    total_noise_pwr = thermal_noise_pwr + quant_error_pwr
    ret = csi * np.sqrt(scale / total_noise_pwr)

    if csi_st.Ntx == 2:
        ret = ret * np.sqrt(2)
    elif csi_st.Ntx == 3:
        ret = ret * np.sqrt(dbinv(4.5))
    
    return ret

def get_scaled_csi_sm(csi_st):
    ret = get_scaled_csi(csi_st)
    ret = remove_sm(ret,csi_st.rate)
    return ret