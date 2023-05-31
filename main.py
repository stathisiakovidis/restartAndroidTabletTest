# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ppadb.client import Client as AdbClient
import os
import time

devices = []


def dump_logcat(connection):
    t_end = time.time() + 30
    while time.time() < t_end:
        data = connection.read(1024)
        if not data:
            break
        print(data.decode('utf-8'))
    print("Close logcat")
    connection.close()


def handlerForHousemate(connection):
    data_str = ""
    while True:
        data = connection.read(1024)
        if not data:
            break
        data_str = data.decode('utf-8')
        print("connection", data_str)
    devices[0].shell("logcat -v threadtime | grep " + data_str, handler=dump_logcat)
    print("Close connection")
    connection.close()
    os.system("adb reboot")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.system("adb start-server")
    client = AdbClient(host="127.0.0.1", port=5037)
    while True:
        devices = []
        print("devices before", devices)
        while len(devices) == 0:
            devices = client.devices()
            time.sleep(20)
            print("devices after", devices)
        if devices[0] is not None:
            print("Connected ", devices[0].get_state())
            devices[0].shell("pidof com.entranet.housematecore", handler=handlerForHousemate)
