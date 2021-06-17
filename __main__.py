import monitor
import monitor_gui


def main():
    processes = monitor.Processes()
    mainWindow = monitor_gui.MainWindow(processes)
    mainWindow.show()


if __name__ == '__main__':
    main()
