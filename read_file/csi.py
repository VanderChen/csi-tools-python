class WifiCsi:

    def __init__(self, args, csi):
        self.timestamp_low = args[0]
        self.bfee_count = args[1]
        self.Nrx = args[2]
        self.Ntx = args[3]
        self.rssi_a = args[4]
        self.rssi_b = args[5]
        self.rssi_c = args[6]
        self.noise = args[7]
        self.agc = args[8]
        self.perm = args[9]
        self.fake_rate_n_flags = args[10]
        self.csi = csi
        pass