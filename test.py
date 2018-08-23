from read_file.read_bf_file import read_file
from csi_proc.get_SNRs import *

def main():
    file_path = 'sample_data/all_csi'
    csi_data = read_file(file_path)
    print(get_mimo2_SNRs(csi_data[16].csi))
    pass

if __name__ == '__main__':
    main()