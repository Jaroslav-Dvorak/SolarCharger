from tkinter import *
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)


#key down funciton
def click():
	entered_text=textentry.get()
	output.delete(0.0, END)
	try:
		definition = my_compdictionary[entered_text]
	except:
		definition = "žádné takové slovo ve slovníku"
	output.insert(END, definition)
	cb1.select()

##### main:
window = Tk()
window.title("test")
#window.configure(background="black")

#create label
Label(window, text="vstupy", font="none 12 bold").grid(row=0, column=0, sticky=W)


def cb21_clicked(pin=21):
	if GPIO.input(pin) == GPIO.HIGH:
		cb21.select()
	else:
		cb21.deselect()
def cb26_clicked(pin=26):
	if GPIO.input(pin) == GPIO.HIGH:
		cb26.select()
	else:
		cb26.deselect()
def cb20_clicked(pin=20):
	if GPIO.input(pin) == GPIO.HIGH:
		cb20.select()
	else:
		cb20.deselect()
def cb16_clicked(pin=16):
	if GPIO.input(pin) == GPIO.HIGH:
		cb16.select()
	else:
		cb16.deselect()
def cb19_clicked(pin=19):
	if GPIO.input(pin) == GPIO.HIGH:
		cb19.select()
	else:
		cb19.deselect()
def cb13_clicked(pin=13):
	if GPIO.input(pin) == GPIO.HIGH:
		cb13.select()
	else:
		cb13.deselect()
def cb12_clicked(pin=12):
	if GPIO.input(pin) == GPIO.HIGH:
		cb12.select()
	else:
		cb12.deselect()

#checkbox
cb21 = Checkbutton(window, text='I21', command=cb21_clicked)
cb21.grid(row=2,column=0, sticky=E)

cb26 = Checkbutton(window, text='I26', command=cb26_clicked)
cb26.grid(row=2,column=1)

cb20 = Checkbutton(window, text='I20', command=cb20_clicked)
cb20.grid(row=2,column=2)

cb16 = Checkbutton(window, text='I16', command=cb16_clicked)
cb16.grid(row=2,column=3)

cb19 = Checkbutton(window, text='I19', command=cb19_clicked)
cb19.grid(row=2,column=4)

cb13 = Checkbutton(window, text='I13', command=cb13_clicked)
cb13.grid(row=2,column=5)

cb12 = Checkbutton(window, text='I12', command=cb12_clicked)
cb12.grid(row=2,column=6)

GPIO.add_event_detect(21, GPIO.BOTH, callback=cb21_clicked)
GPIO.add_event_detect(26, GPIO.BOTH, callback=cb26_clicked)
GPIO.add_event_detect(20, GPIO.BOTH, callback=cb20_clicked)
GPIO.add_event_detect(16, GPIO.BOTH, callback=cb16_clicked)
GPIO.add_event_detect(19, GPIO.BOTH, callback=cb19_clicked)
GPIO.add_event_detect(13, GPIO.BOTH, callback=cb13_clicked)
GPIO.add_event_detect(12, GPIO.BOTH, callback=cb12_clicked)


#create label
Label(window, text="výstupy", font="none 12 bold").grid(row=3, column=0, sticky=W)

#create label
varcb6 = IntVar()
varcb5 = IntVar()
varcb22 = IntVar()
varcb27 = IntVar()
varcb17 = IntVar()

def cb6_clicked():
	if varcb6.get() == 1:
		GPIO.output(6, True)
	else:
		GPIO.output(6, False)
def cb5_clicked():
	if varcb5.get() == 1:
		GPIO.output(5, True)
	else:
		GPIO.output(5, False)
def cb22_clicked():
	if varcb22.get() == 1:
		GPIO.output(22, True)
	else:
		GPIO.output(22, False)
def cb27_clicked():
	if varcb27.get() == 1:
		GPIO.output(27, True)
	else:
		GPIO.output(27, False)
def cb17_clicked():
	if varcb17.get() == 1:
		GPIO.output(17, True)
	else:
		GPIO.output(17, False)

#checkbox
cb6 = Checkbutton(window, text='O6', command=cb6_clicked, variable=varcb6)
cb6.grid(row=4,column=0, sticky=E)

cb5 = Checkbutton(window, text='O5', command=cb5_clicked, variable=varcb5)
cb5.grid(row=4,column=1)

cb22 = Checkbutton(window, text='O22', command=cb22_clicked, variable=varcb22)
cb22.grid(row=4,column=2)

cb27 = Checkbutton(window, text='O27', command=cb27_clicked, variable=varcb27)
cb27.grid(row=4,column=3)

cb17 = Checkbutton(window, text='O17', command=cb17_clicked, variable=varcb17)
cb17.grid(row=4,column=4)


def close_window():
	window.destroy()
	exit()

#add a exit button
Button(window, text="Exit", width=14, command=close_window).grid(row=7, column=0, sticky=W)


window.mainloop()

GPIO.cleanup()
