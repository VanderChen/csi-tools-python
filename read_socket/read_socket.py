import ctypes
import multiprocessing
import time
import logging

from ..read_file import read_bf_file


def make_data(read_event, make_event, read_count, group_num):
    while True:
        make_event.wait()
        for file_order in range(read_count):
            so.buf_file_open(group_num, file_order)
            check = so.start_read(group_num, file_order)
            if check == 0:
                so.buf_file_close(group_num, file_order)
        make_event.clear()
        read_event.set()
    pass


def read_data(read_event, make_event, file_group, file_order, csi_list, logger):
    while True:
        read_event.wait()
        try:
            csi = read_bf_file.read_file("buf_data" + str(file_group) + str(file_order))
            if(len(csi) != 0):
                csi_list.append(csi[0])
        except Exception as e:
            logger.info(e)
        read_event.clear()
        make_event.set()
    pass


def timestamp(csi):
    return csi.timestamp_low


def sort_data(csi_list, make_count, read_count_per_make, csi_lock, count_gap):
    count = make_count * read_count_per_make
    current_time = time.time()
    out_count = 0
    while True:
        if out_count > count_gap:
            start_time = current_time
            current_time = time.time()
            print(count_gap / (current_time - start_time), "pkt/s")
            out_count -= count_gap
        if len(csi_list) >= count * 2:

            csi_lock.acquire()
            sorted_data = sorted(csi_list, key=timestamp)
            # for csi in sorted_data[:count]:
            #     print(csi.timestamp_low)
            #     pass
            out_count += count
            csi_list[:] = []
            csi_list.extend(sorted_data[count + 1:])
            csi_lock.release()


def read_socket_start():
    make_count = 10
    read_count_per_make = 8
    sort_count = 1
    count_gap = 1000

    global so
    so = ctypes.CDLL("csi-tools-python/c_lib/log_to_file.so")
    so.init_socket(b"log_data")

    read_event = []
    make_event = []

    make_process = []
    read_process = []
    sort_process = []

    for _ in range(make_count):
        read_event.append(multiprocessing.Event())
    for _ in range(make_count):
        make_event.append(multiprocessing.Event())
    csi_list = multiprocessing.Manager().list()
    csi_lock = multiprocessing.Lock()
    logger = logging.getLogger('error_log')

    for i in range(make_count):
        make_process.append(multiprocessing.Process(
            name="make_data" + str(i), target=make_data, args=(read_event[i], make_event[i], read_count_per_make, i,)))

    for i in range(make_count):
        for j in range(read_count_per_make):
            read_process.append(multiprocessing.Process(
                name="read_data" + str(i), target=read_data, args=(read_event[i], make_event[i], i, j, csi_list, logger,)))

    for i in range(sort_count):
        sort_process.append(multiprocessing.Process(name="sort_data" + str(i), target=sort_data,
                                                    args=(csi_list, make_count, read_count_per_make, csi_lock, count_gap,)))

    for p in make_process:
        p.start()
    for p in read_process:
        p.start()
    for p in sort_process:
        p.start()

    for e in make_event:
        e.set()

    for p in make_process:
        p.join()
    for p in read_process:
        p.join()
    for p in sort_process:
        p.join()

