from tkinter import *
from tkinter.ttk import *
from MPPTvars import variables

class GUI:
    def __init__(self):
        self.geometry = "800x600+50+50"
        self.title = "Selector"
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback_exit)
        self.root.title(self.title)
        self.root.geometry(self.geometry)

        self.ConnectFrame = Frame(self.root)
        self.ConnectFrame.grid(column=0, row=0, sticky=W)

        self.RatedFrame = Frame(self.root)
        self.RatedFrame.grid(column=0, row=1)

        self.RealTimeFrame = Frame(self.root)
        self.RealTimeFrame.grid(column=0, row=2)

        self.IPlabel = Label(self.ConnectFrame, text="IP:")
        self.IPlabel.grid(column=0, row=0)
        self.IPentry = Entry(self.ConnectFrame)
        self.IPentry.configure(width=13)
        self.IPentry.grid(column=1, row=0)
        self.portLabel = Label(self.ConnectFrame, text="port:")
        self.portLabel.grid(column=2, row=0)
        self.portEntry = Entry(self.ConnectFrame)
        self.portEntry.configure(width=5)
        self.portEntry.grid(column=3, row=0)
        self.ConnectButton = Button(self.ConnectFrame, text="connect", command=self.show_rated_data)
        self.ConnectButton.grid(column=4, row=0)

        self.RatedLabels = []
        self.RatedEntrys = []

        self.root.mainloop()

    def callback_exit(self):
        self.root.destroy()
        self.root.quit()

    def show_rated_data(self):
        self.RatedLabel = Label(self.RatedFrame, text="RATED DATA", font=('Helvetica', 18, 'bold'))
        self.RatedLabel.grid(column=0, row=0, columnspan=2)
        for index, label in enumerate(variables["rated data"], 1):
            self.RatedLabels.append(Label(self.RatedFrame, text=label))
            self.RatedLabels[-1].grid(column=0, row=index, sticky=E)
            self.RatedEntrys.append(Entry(self.RatedFrame, width=20))
            self.RatedEntrys[-1].insert(0, "1234")
            self.RatedEntrys[-1].configure(state="readonly")
            self.RatedEntrys[-1].grid(column=1, row=index)


gui = GUI()
