#!/usr/bin/python

from __future__ import print_function
import Tkinter
from Logger import Logger
import argparse
from ShutdownMaintainer import ShutdownMaintainer
from ShutdownMaintainer import ShutdownException
import sys
import os


class ShutdownApp(Tkinter.Tk):
    def __init__(self, args,logger):
        Tkinter.Tk.__init__(self)
        self._contentUpdated = True
        self.time = args.hour
        self._delayedTime = args.hour
	self.logger = logger
        self.initialiase()
        self.title("Shutdown")

    def initialiase(self):
        self.geometry("450x100+100+100")
        self.container = Tkinter.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for f in (NotifyFrame, DelayFrame, DelayedFrame):
            frame = f(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[f] = frame
        self.show_frame(NotifyFrame)

    def update_frames(self):
        if self._contentUpdated:
            self._contentUpdated = False
            for f in (NotifyFrame, DelayFrame, DelayedFrame):
                frame = f(self.container, self)
                frame.grid(row=0, column=0, sticky="nsew")
                self.frames[f] = frame

    def show_frame(self, class_name):
        # need to refresh frame on raising
        self.update_frames()
        self.frames[class_name].tkraise()

    def set_delayed_time(self, value):
        self._delayedTime = value
        self._contentUpdated = True

    def get_delayed_time(self):
        return self._delayedTime


class ShutdownLabel(Tkinter.Label):
    def __init__(self, master):
        Tkinter.Label.__init__(self, master)
        self.configure(font=("Helvetica", 16), fg="black")


class BaseFrame(Tkinter.Frame):
    def __init__(self, master, controller):
        Tkinter.Frame.__init__(self, master)
        self.controller = controller
        self.populate()

    def dispatch(self, frame):
        self.controller.show_frame(frame)

    def populate(self):
        raise NotImplementedError


class NotifyFrame(BaseFrame):
    def populate(self):
        self.label = ShutdownLabel(self)
        self.label.configure(bg="red")
        self.label.config(text="System will shutdown at {}:00".format(self.controller.time))
        self.label.pack(fill="x")
        self.delay_button = Tkinter.Button(self, text="DELAY", command=lambda: self.dispatch(DelayFrame))
        self.delay_button.pack(pady=1, padx=10)


class DelayFrame(BaseFrame):
    def populate(self):
        self.label = ShutdownLabel(self)
        self.label.configure(bg="white")
        self.label['text'] = "Enter the number of hours to delay shutdown:"
        self.label.pack(fill="x")
        self.entry = Tkinter.Entry(self)
        self.entry.pack(fill="x")
        self.continue_button = Tkinter.Button(self, text="DELAY", command=lambda: self.dispatch(DelayedFrame))
        self.continue_button.pack(pady=1, padx=10)

    """ Override BaseFrame.dispatch
        calls Shutdown_maintainer to cancel and then
        set a shutdown for the requested time"""
    def dispatch(self, frame):
        self.controller.set_delayed_time(int(self.entry.get()) + self.controller.time)
        if args.verbose:
            print("Canceling shutdown.. ")
        maintainer = ShutdownMaintainer(self.controller.logger)
        try:
            maintainer.cancel_shutdown()
        except ShutdownException:
            if args.verbose:
                print("Error canceling shutdown closing", file=sys.stderr)
            sys.exit(1)

        if args.verbose:
            print("Shutdown canceled..")
            print("setting new shutdown for {0}:00..".format(self.controller.get_delayed_time()))

        try:
            maintainer.set_shutdown(int(self.entry.get()))
        except ShutdownException:
            if args.verbose:
                print("Error setting new shutdown closing", file=sys.stderr)

        if args.verbose:
            print("Shutdown Delayed until {0}:00".format(self.controller.get_delayed_time()))

        BaseFrame.dispatch(self, frame)


class DelayedFrame(BaseFrame):
    def populate(self):
        self.label = ShutdownLabel(self)
        self.label.configure(bg="white")
        self.label.config(text="Shutdown Delayed until {0}".format(self.controller.get_delayed_time()))
        self.label.pack(fill="x")


def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('hour', type=int, help='The hour that shutdown is set for')
    parser.add_argument('-v', '--verbose', help='prints everything', action='store_true')
    parser.add_argument('-l','--log',default='',help='The path where the log file will be created')
    return parser.parse_args()

if __name__ == '__main__':
    args = build_args()
    if not os.geteuid() == 0:
        sys.exit('Script must be run as root')
    
    logger = Logger('{0}shutdown.log'.format(args.log))

    if args.verbose:
        logger.log('Script started')

    app = ShutdownApp(args, logger)
    app.mainloop()

    if args.verbose:
        logger.log('Script finished\n')
    logger.close()

