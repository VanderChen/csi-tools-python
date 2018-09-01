from read_file.read_bf_file import read_file

def main():
    file_path = 'sample_data/test_data'
    csi_data = read_file(file_path)
    for csi in csi_data:
        print(csi.csi)
    # print(csi_data[28].Ntx)
    # print(get_scaled_csi_sm(csi_data[28]))
    pass

if __name__ == '__main__':
    main()