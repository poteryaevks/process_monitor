import tkinter as tk
import tkinter.ttk as ttk


def sortFunc(tv, column, comp, reverse):
    tempList = [(tv.set(k, column), k) for k in tv.get_children('')]
    tempList = sorted(tempList, key=comp, reverse=reverse())

    for index, (val, k) in enumerate(tempList):
        tv.move(k, '', index)


def pidExists(tv, pid):

    tempList = []
    for k in tv.get_children(''):
        if int(tv.set(k, 1)) == pid:
            tempList.append(int(tv.set(k, 1)))

    if len(tempList) > 0:
        return True
    else:
        return False


class ProcessTable(tk.Frame):

    size = 0

    sorter = {
        '#1': lambda row: int(row[0]),
        '#2': lambda row: int(row[0]),
        '#3': lambda row: str(row[0]).lower(),
        '#4': lambda row: str(row[0]).lower()
    }

    column = {
        '#1': 0,
        '#2': 1,
        '#3': 2,
        '#4': 3
    }

    reverser = {
        '#1': False,
        '#2': False,
        '#3': False,
        '#4': False
    }

    header = ['Number', 'Pid', 'Name', 'User']

    def __init__(self, parent=None):

        super().__init__(parent)
        self.table = ttk.Treeview(self, show="headings", selectmode="browse")
        self.table["columns"] = self.header
        self.table["displaycolumns"] = self.header

        for head in self.header:
            self.table.heading(head, text=head, anchor=tk.CENTER)
            self.table.column(head, anchor=tk.CENTER)

        scroll_table = tk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=scroll_table.set)
        scroll_table.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

        self.table.bind("<ButtonRelease-1>", self.OnReleaseCallback)

    def insert(self, rows):
        self.table.insert('', tk.END, values=rows)

    def clear(self):
        for item in self.table.get_children():
            self.table.delete(item)

    def OnReleaseCallback(self, event):
        region = self.table.identify("region", event.x, event.y)
        if region == "heading":
            column = self.table.identify_column(event.x)

            def checkReverse():
                if self.reverser[column]:
                    self.reverser[column] = False
                    return True
                else:
                    self.reverser[column] = True
                    return False

            sortFunc(self.table, self.column[column], self.sorter[column], checkReverse)

    def update(self, ps):
        """ сохранить актуальные """
        pids = []

        for p in ps:
            pids.append(p.pid)
            if not pidExists(self.table, p.pid):
                self.size += 1
                self.insert((self.size, p.pid, p.name(), p.username()))

        """ убить устаревшие """
        for child in self.table.get_children(''):
            pid = self.table.set(child, 1)
            if len([p for p in pids if int(pid) == p]) == 0:
                self.table.delete(child)


class MainWindow:
    title = "Process monitor"

    def __init__(self):
        self.window = tk.Tk()
        self.window.title(self.title)
        self.table = ProcessTable(self.window)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

    def show(self):
        self.window.mainloop()

    def getTable(self):
        return self.table
