import tkinter as tk
import tkinter.font as tkFont
from tkinter import scrolledtext
import psutil
import threading
import multiprocessing
import sys

from tkinter import ttk

import time
import datetime

class OverwatchBlocker:
    def __init__(self):
        self.blocker = True
        self.window = tk.Tk()
        self.window.title("Overwatch Blocker")
        self.thread = threading.Thread(target=self.bnet_blocker)
        self.thread.daemon = False
        self.status = tk.Label(self.window, text="")
        self.timer_options = []
        self.minimized = False

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.container = tk.Frame(self.window, bg='lightgrey', padx=20, pady=20)
        self.container.pack(fill="both", expand=True)

        self.toggle_var = "timer"

        self.logging_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=500, height=300)

        self.start_app()

    # def __del__(self):
    #     self.thread.join()
    #     self.timerthread.join()

    def on_closing(self):
        self.window.withdraw()
        self.minimized = True

    def stop_blocking_text(self):
        if hasattr(self, 'status'):
            self.status.config(text="Overwatch is not being blocked anymore. Have Fun!")
        if hasattr(self, 'time_display'):
            self.time_display.config(text="")

        if self.minimized == True:
            self.window.destroy()
            sys.exit()

    def bnet_blocker(self):
        while self.blocker:
            for program in psutil.process_iter():
                if program.name() == "Battle.net.exe" or program.name() == "Overwatch.exe":
                    try:
                        pid = program.pid
                        process = psutil.Process(pid)
                        process.terminate()

                        self.logging_text.insert(tk.END, datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ": Blocking " + program.name() + "\n")
                        self.logging_text.see(tk.END)
                    except:
                        pass
            time.sleep(1)
        self.window.after(0, self.stop_blocking_text)

            
    def start_blocker(self):
        self.init_blocker()
        self.status.config(text="Overwatch is being blocked.")
        self.blocker = True
        self.thread.start()

    def init_blocker(self):
        if self.thread.is_alive():
            self.blocker = False
            self.thread.join()

        self.thread = threading.Thread(target=self.bnet_blocker)
        self.thread.daemon = False

    def completed_drawing(self):
        self.blocker = False
    
    def start_timer(self):
        self.start_blocker()
        inputted_time = datetime.timedelta(hours=int(self.timer_options[0].get() + self.timer_options[1].get()),
                                minutes=int(self.timer_options[2].get() + self.timer_options[3].get()),
                                seconds=int(self.timer_options[4].get() + self.timer_options[5].get()))
            
        maxtime = inputted_time.total_seconds()
        self.timerthread = threading.Thread(target=self.timer_function, args=(maxtime,))
        self.timerthread.start()

    def timer_function(self, maxtime):
        self.curr_time = int(maxtime)
        while (self.curr_time > 0):
            self.curr_time -= 1
            time_delta = datetime.timedelta(seconds=self.curr_time)
            self.time_display.config(text="Remaining Time: " + str(time_delta))
            time.sleep(1)
        self.blocker = False
        return

    def create_timer(self):
        self.init_blocker()
        counter = 0
        for i in range(6):
            option_list = []
            if i % 2 == 0:
                option_list = ["0", "0", "1", "2", "3", "4", "5"]
            else:
                option_list = ["0", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

            base_timer_text = tk.StringVar(self.container)
            base_timer_text.set(option_list[0])

            tmp = ttk.OptionMenu(self.container, base_timer_text, *option_list)
            tmp.pack(side="left")
            counter += 1
            self.timer_options.append(base_timer_text)

            if i % 2 == 1 and i != 5:
                tmp_font = tkFont.Font(family="Arial", size=12)

                spacing = tk.Label(self.container, bg="lightgray", text="", font=tmp_font)
                spacing.pack(side="left")

                tmp_text = tk.Label(self.container, bg="lightgray", text=":", font=tmp_font)
                tmp_text.pack(side="left")

                spacing2 = tk.Label(self.container, bg="lightgray", text="", font=tmp_font)
                spacing2.pack(side="left")



        

        button_font = tkFont.Font(family="Arial", size=16)
        timer_button = tk.Button(self.container, text="Start Timer", command=self.start_timer, font=button_font)
        timer_button.pack(side="bottom")

    def create_button(self):
        self.start_blocker()
        button_font = tkFont.Font(family="Arial", size=16)
        drawing_complete = tk.Button(self.container, text="Completed Drawing", command=self.completed_drawing, font=button_font)
        drawing_complete.pack()

    def toggle_func(self):
        self.destroy_container()
        
        if self.toggle_var == "timer":
            if hasattr(self, 'timerthread') and self.timerthread.is_alive():
                self.curr_time = 0
                self.timerthread.join()

            self.toggle_var = "button"
            self.create_button()
            self.toggle.config(text="Button")
            self.time_display.config(text="")
            self.status.config(text="Overwatch is being blocked.")
        else:
            self.toggle_var = "timer"
            self.create_timer()
            self.toggle.config(text="Timer")
            self.status.config(text="")

    def destroy_container(self):
        self.timer_options = []
        for widget in self.container.winfo_children():
            widget.destroy()

    def start_app(self):
        #self.thread.start()

        self.window.geometry("600x600")

        title_font = tkFont.Font(family="Arial", size=24)

        title = tk.Label(self.window, text="Overwatch Blocker", font=title_font)
        title.pack()

        space = tk.Label(self.window, text="")
        space.pack()

        button_font = tkFont.Font(family="Arial", size=16)

        self.toggle = tk.Button(self.window, text="Timer", command=self.toggle_func, font=button_font)
        self.toggle.pack()

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