import getpass
import psutil


class Processes:

    processes = [{}]
    needRevers = False

    def __init__(self, parent=None):
        self.currentComp = lambda p: p['pid']

        for process in psutil.process_iter():
            self.processes.append({'pid': process.pid,
                                   'name': process.name(),
                                   'user': process.username()}
                                  )

    def setSorter(self, comp, reverse):
        self.currentComp = comp
        self.needRevers = reverse()
        self.update()

    def update(self):
        self.processes.clear()
        for process in psutil.process_iter():
            self.processes.append({'pid': process.pid,
                                   'name': process.name(),
                                   'user': process.username()}
                                  )

        self.processes = sorted(self.processes,
                                key=self.currentComp,
                                reverse=self.needRevers)

    def __iter__(self):
        for process in self.processes:
            # if getpass.getuser() == process['user'].split('\\')[-1]:
                yield process
