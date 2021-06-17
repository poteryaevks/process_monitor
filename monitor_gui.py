import tkinter as tk
import tkinter.ttk as ttk


# def sortFunc(tv, column, comp, reverse):
#     tempList = [(tv.set(k, column), k) for k in tv.get_children('')]
#     tempList = sorted(tempList, key=comp, reverse=reverse())
#
#     for index, (val, k) in enumerate(tempList):
#         tv.move(k, '', index)


def getByPid(tv, pid):
    for item in tv.get_children(''):
        if pid == int(tv.set(item, 0)):
            return item
    return None


def getRowNumber(tv, item):

    for count, i in enumerate(tv.get_children('')):
        if i == item[0]:
            return count
    return None


def pidExists(tv, pid):

    tempList = []
    for k in tv.get_children(''):
        if int(tv.set(k, 0)) == pid:
            tempList.append(int(tv.set(k, 0)))

    if len(tempList) > 0:
        return True
    else:
        return False


def inScrollArea(tv, row):
    style = ttk.Style(tv)
    rowsInTable = float(len(tv.get_children('')))
    rowHeight = float(style.lookup('Treeview', 'rowheight'))
    border = tv.yview()
    lowerBorder = rowsInTable * rowHeight * float(border[0])
    upperBorder = rowsInTable * rowHeight * float(border[1])
    rowPos = row * rowHeight

    if rowPos >= upperBorder or rowPos <= lowerBorder:
        return False
    else:
        return True


class ProcessTable(tk.Frame):

    processes = None

    comp = {
        '#1': lambda process: process['pid'],
        '#2': lambda process: process['name'].lower(),
        '#3': lambda process: process['user'].lower()
    }

    column = {
        '#1': 1,
        '#2': 2,
        '#3': 3
    }

    reverser = {
        '#1': False,
        '#2': False,
        '#3': False
    }

    header = ['Pid', 'Name', 'User']

    def __init__(self, parent=None):

        super().__init__(parent)
        self.newSorter = False

        self.table = ttk.Treeview(self, show="headings", selectmode="browse")
        style = ttk.Style(self.table)
        style.configure("Treeview.Heading", font=(None, 15), rowheight=40)
        style.configure("Treeview", font=(None, 15), rowheight=40)

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
        self.table.bind("<Control-MouseWheel>",  self.OnWheelCallback)
        self.table.bind("<KeyPress>", self.OnKeyCallback)
        self.table.bind("<<TreeviewSelect>>", self.ItemChangedCallback)

    def insert(self, rows):
        self.table.insert('', tk.END, values=rows)

    def clear(self):
        for item in self.table.get_children():
            self.table.delete(item)

    def OnKeyCallback(self, event):
        for process in self.processes:
            if process['name'].lower()[0] == event.char:
                item = getByPid(self.table, process['pid'])
                self.table.selection_set(item)
                break

    def ItemChangedCallback(self, event):
        row = getRowNumber(self.table, self.table.selection())
        if not inScrollArea(self.table, row):
            self.table.yview_moveto(row / len(self.table.get_children('')))

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

            self.processes.setSorter(self.comp[column],
                                     checkReverse
                                     )

            self.newSorter = True
            self.table.yview_moveto(-1)

    def OnWheelCallback(self, event):
        style = ttk.Style(self.table)
        strFont = style.lookup('Treeview', 'font')
        currentFont = [int(s) for s in strFont.split() if s.isdigit()]

        if event.delta > 0 and not currentFont[-1] > 20:
            currentFont[-1] += 1
        if event.delta < 0 and not currentFont[-1] < 15:
            currentFont[-1] -= 1

        style.configure("Treeview.Heading", font=(None, currentFont[-1]), rowheight=40)
        style.configure("Treeview", font=(None, currentFont[-1]), rowheight=40)

    def updateTable(self):
        self.processes.update()
        currentPidList = []

        if self.newSorter:
            self.clear()
            for process in self.processes:
                self.insert((process['pid'],
                             process['name'],
                             process['user']
                             ))
        else:
            ''' сохранить актуальные '''
            for process in self.processes:
                currentPidList.append(process['pid'])
                if not pidExists(self.table, process['pid']):
                    self.insert((process['pid'],
                                 process['name'],
                                 process['user']
                                 ))

            ''' убить устаревшие '''
            for child in self.table.get_children(''):
                pid = self.table.set(child, 0)
                if len([p for p in currentPidList if int(pid) == p]) == 0:
                    self.table.delete(child)

        self.newSorter = False


class MainWindow:

    title = "Process monitor"

    def __init__(self, processes):
        self.window = tk.Tk()
        self.window.title(self.title)
        self.table = ProcessTable(self.window)
        self.table.processes = processes
        self.table.pack(expand=tk.YES, fill=tk.BOTH)
        self.window.after(50, self.update)

    def show(self):
        self.window.mainloop()

    def getTable(self):
        return self.table

    def update(self):
        self.table.updateTable()
        self.window.after(50, self.update)


