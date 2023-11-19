import tkinter as tk
import tkinter.font as tkFont
import psutil
import threading

import time

class OverwatchBlocker:
    def __init__(self):
        self.blocker = True
        self.window = tk.Tk()
        self.thread = threading.Thread(target=self.bnet_blocker)
        self.status = tk.Label(self.window, text="Overwatch/Bnet is being blocked.")

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
                    print("Terminating " + str(program.name()))
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



        self.window.mainloop()