#!/usr/bin/python

import Tkinter


class Shutdown_app(Tkinter.Tk):
	def __init__(self):
		Tkinter.Tk.__init__(self)
		self.initialiase()
		self.title("Shutdown")

	def initialiase(self):
		self.container = Tkinter.Frame(self)
		self.container.grid(row=0,column=0)

		self.frames = {}
		for f in (Notify_Frame,Delay_Frame):
			frame = f(self.container,self)
			frame.grid(row=2,column=2, sticky=Tkinter.NW+Tkinter.SE)
			self.frames[f] = frame
		self.show_frame(Notify_Frame)

	def show_frame(self,class_name):
		self.frames[class_name].tkraise()

class Base_Frame(Tkinter.Frame):
	def __init__(self, master, controller):
		Tkinter.Frame.__init__(self, master)
		self.controller = controller
		self.grid()
		self.populate()

	def populate(self):
		raise NotImplementedError


class Notify_Frame(Base_Frame):
	def populate(self):
		self.label = Tkinter.Label(self, anchor="n", fg="black", bg="white")
		self.label.grid(column=0, row=0)
		self.label['text'] = "Shutdown imminent"
		self.delay_button = Tkinter.Button(self, anchor="s",text="DELAY", command=lambda: self.controller.show_frame(Delay_Frame))
		self.delay_button.grid(column=0,row=1);


class Delay_Frame(Base_Frame):
	def populate(self):
		self.label = Tkinter.Label(self, anchor="n", fg="black", bg="white")
		self.label.grid(column=0, row=0)
		self.label['text'] = "Shutdown Delayed"


if __name__ == '__main__':
	app = Shutdown_app()
	app.mainloop()



