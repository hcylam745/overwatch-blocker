import tkinter as tk
import tkinter.font as tkFont
from tkinter import scrolledtext
import psutil
import threading

import time
import datetime

class OverwatchBlocker:
    def __init__(self):
        self.blocker = True
        self.window = tk.Tk()
        self.window.title("Overwatch Blocker")
        self.thread = threading.Thread(target=self.bnet_blocker)
        self.status = tk.Label(self.window, text="Overwatch/Bnet is being blocked.")

        self.logging_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=500, height=300)

        self.start_app()

    def __del__(self):
        self.thread.join()

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
        self.blocker = False
        self.thread.join()
        self.status.config(text="Overwatch is not being blocked anymore. Have Fun!")

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

        gap = tk.Label(self.window, text="")
        gap.pack()
        self.status.pack()

        space2 = tk.Label(self.window, text="\n\n")
        space2.pack()

        logs_label = tk.Label(self.window, text="Logs", font=button_font)
        logs_label.pack()

        self.logging_text.pack(expand=True, fill=tk.BOTH)



        self.window.mainloop()