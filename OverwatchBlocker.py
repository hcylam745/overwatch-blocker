import tkinter as tk
import tkinter.font as tkFont
from tkinter import scrolledtext
import psutil
import threading

from tkinter import ttk

import time
import datetime

class OverwatchBlocker:
    def __init__(self):
        self.blocker = True
        self.window = tk.Tk()
        self.window.title("Overwatch Blocker")
        self.thread = threading.Thread(target=self.bnet_blocker)
        self.status = tk.Label(self.window, text="Overwatch/Bnet is being blocked.")
        self.timer_options = []

        self.logging_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=500, height=300)

        self.start_app()

    def __del__(self):
        self.thread.join()
        self.timerthread.join()

    def bnet_blocker(self):
        while self.blocker:
            for program in psutil.process_iter():
                if program.name() == "Battle.net.exe" or program.name() == "Overwatch.exe":
                    pid = program.pid
                    process = psutil.Process(pid)
                    process.terminate()

                    self.logging_text.insert(tk.END, datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ": Blocking " + program.name() + "\n")
                    self.logging_text.see(tk.END)
            time.sleep(15)

    def completed_drawing(self):
        #print("completed drawing called")
        self.blocker = False
        self.thread.join()
        self.status.config(text="Overwatch is not being blocked anymore. Have Fun!")
    
    def start_timer(self):
        #print("starting timer")
        #maxtime = self.timeinput.get()
        inputted_time = datetime.timedelta(hours=int(self.timer_options[0].get() + self.timer_options[1].get()),
                                minutes=int(self.timer_options[2].get() + self.timer_options[3].get()),
                                seconds=int(self.timer_options[4].get() + self.timer_options[5].get()))
            
        maxtime = inputted_time.total_seconds()

        #print(maxtime)
        self.timerthread = threading.Thread(target=self.timer_function, args=(maxtime,))
        self.timerthread.start()

    def timer_function(self, maxtime):
        #print("timer started.")
        curr_time = int(maxtime)
        while (curr_time > 0):
            curr_time -= 1
            time_delta = datetime.timedelta(seconds=curr_time)
            self.time_display.config(text="Remaining Time: " + str(time_delta))
            #print("curr_time = " + str(curr_time))
            time.sleep(1)
        #print("completed drawing")
        self.completed_drawing()
        return

    def create_timer(self):
        #print("creating timer")

        timer_container = tk.Frame(self.window, bg='lightgrey', padx=20, pady=20)
        timer_container.pack(fill="both", expand=True)

        counter = 0
        for i in range(6):
            option_list = []
            if i % 2 == 0:
                option_list = ["0", "0", "1", "2", "3", "4", "5"]
            else:
                option_list = ["0", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

            base_timer_text = tk.StringVar(timer_container)
            base_timer_text.set(option_list[0])

            tmp = ttk.OptionMenu(timer_container, base_timer_text, *option_list)
            tmp.pack(side="left")
            counter += 1
            self.timer_options.append(base_timer_text)

            if i % 2 == 1 and i != 5:
                tmp_font = tkFont.Font(family="Arial", size=12)

                spacing = tk.Label(timer_container, bg="lightgray", text="", font=tmp_font)
                spacing.pack(side="left")

                tmp_text = tk.Label(timer_container, bg="lightgray", text=":", font=tmp_font)
                tmp_text.pack(side="left")

                spacing2 = tk.Label(timer_container, bg="lightgray", text="", font=tmp_font)
                spacing2.pack(side="left")



        

        button_font = tkFont.Font(family="Arial", size=16)
        timer_button = tk.Button(timer_container, text="Start Timer", command=self.start_timer, font=button_font)
        timer_button.pack(side="bottom")

    def start_app(self):
        self.thread.start()

        self.window.geometry("600x600")

        title_font = tkFont.Font(family="Arial", size=24)

        title = tk.Label(self.window, text="Overwatch Blocker", font=title_font)
        title.pack()

        space = tk.Label(self.window, text="")
        space.pack()

        button_font = tkFont.Font(family="Arial", size=16)

        drawing_complete = tk.Button(self.window, text="Completed Drawing", command=self.completed_drawing, font=button_font)
        drawing_complete.pack()

        self.create_timer()

        self.time_display = tk.Label(self.window, text="")
        self.time_display.pack()
        self.status.pack()

        space2 = tk.Label(self.window, text="\n\n")
        space2.pack()

        logs_label = tk.Label(self.window, text="Logs", font=button_font)
        logs_label.pack()

        self.logging_text.pack(expand=True, fill=tk.BOTH)



        self.window.mainloop()