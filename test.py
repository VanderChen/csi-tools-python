from read_file.read_bf_file import read_file
from csi_proc.get_SNRs import get_simo_SNRs

def main():
    file_path = 'sample_data/all_csi'
    csi_data = read_file(file_path)
    print(get_simo_SNRs(csi_data[0].csi))
    pass

if __name__ == '__main__':
    main()