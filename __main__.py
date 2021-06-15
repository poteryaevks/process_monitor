import threading
import time

import monitor
import monitor_gui


def worker(t, ps):
    while True:
        t.update(ps)
        time.sleep(0.05)


if __name__ == '__main__':

    mainWindow = monitor_gui.MainWindow()
    table = mainWindow.getTable()
    processes = monitor.Processes()

    thread = threading.Thread(target=worker, args=(table, processes))
    thread.start()

    mainWindow.show()
