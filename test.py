from .read_socket import read_socket

def main():
    read_socket.read_socket_start()
    while True:
        print(read_socket.out_data.get())
    pass

if __name__ == '__main__':
    main()