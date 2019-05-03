import tkinter as tk
from threading import Thread, Event
from tkinter import filedialog
import vlc
import time
from tkinter import ttk


class Screen(tk.Frame):

    def GetHandle(self):
        #frame ID
        return self.videopanel.winfo_id()

    def chooseFile(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=(("mp4 files", "*.mp4"), ("mkv files", "*.mkv"),("avi files", "*.avi"),("mp3 files", "*.mp3")))
        root.update()
        return file_path

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.settings = {
            "width" : 1024,
            "height" : 576,
        }
        self.parent=parent
        self.settings.update(kwargs)

        self.video_source = self.chooseFile()
        self.videopanel = ttk.Frame(self)
        self.canvas = tk.Canvas(self.videopanel,  bg="black").pack(fill=tk.BOTH, expand=1)
        self.videopanel.pack(fill=tk.BOTH, expand=1)

        ctrlpanel = ttk.Frame(self)
        ctrlpanel4=ttk.Frame(ctrlpanel)
        self.play_photo = tk.PhotoImage(file="play.png")
        play = ttk.Button(ctrlpanel4)
        play.config(image=self.play_photo, command=self.play)
        #play.grid(column=1, row=1, sticky=(tk.E, tk.W))

        self.pause_photo= tk.PhotoImage(file="pause.png")
        pause = ttk.Button(ctrlpanel4)
        pause.config(image=self.pause_photo, command=self.pause)
        #pause.grid(column=2, row=1, sticky=(tk.E, tk.W))

        self.stop_photo = tk.PhotoImage(file="stop.png")
        stop = ttk.Button(ctrlpanel4)
        stop.config(image=self.stop_photo, command=self.stop)
        #stop.grid(column=3, row=1, sticky=(tk.E, tk.W))

        pause.pack(side=tk.LEFT)
        play.pack(side=tk.LEFT)
        stop.pack(side=tk.LEFT)

        ctrlpanel3 = ttk.Frame(ctrlpanel)

        self.volume_var = tk.IntVar()
        self.volume_var.set(50)

        self.volslider = tk.Scale(ctrlpanel3, variable=self.volume_var,
                                  from_=100, to=0, orient=tk.VERTICAL, length=65 ,command=self.volume_seek)####################
        self.volslider.pack(side=tk.LEFT)
        ctrlpanel.pack(side=tk.BOTTOM, fill=tk.X)


        ctrlpanel3.pack(side=tk.RIGHT)
        ctrlpanel4.pack()

        ctrlpanel2 = ttk.Frame(self)
        self.scale_var = tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = tk.Scale(ctrlpanel2, variable=self.scale_var,
                                   from_=0, to=1000, orient=tk.HORIZONTAL, length=500,command=self.seek)####################
        self.timeslider.pack(side=tk.BOTTOM, fill=tk.X, expand=1)
        self.timeslider_last_update = time.time()
        ctrlpanel2.pack(side=tk.BOTTOM, fill=tk.X)

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        Media = self.instance.media_new(self.video_source)
        Media.get_mrl()
        self.player.set_media(Media)
        self.player.set_hwnd(self.GetHandle())



        self.timer = timerThread(self.timeCounter, 1.0)
        self.timer.start()

        #initialize
        self.player.audio_set_volume(50)
        self.play()


    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
        self.timeslider.set(0)

    def quit(self):
        self.quit()

    def timeCounter(self):
        #range calculations and fitting
        length = self.player.get_length()
        interval = length * 0.001
        self.timeslider.config(to=interval)
        # slider time
        player_time = self.player.get_time()
        second = player_time * 0.001 # milisecond to second
        self.timeslider_last_val = ("%.0f" % second) + ".0"
        self.timeslider.set(second)

    def seek(self, evt):
        if self.player == None:
            return
        int_val = self.scale_var.get()
        str_val = str(int_val)
        if self.timeslider_last_val != str_val:#kullanıcı oynayınca calısıyor
            self.timeslider_last_update = time.time()
            val = "%.0f" % (int_val * 1000)
            self.player.set_time(int(val))  #milisecond

    def volume_seek(self, evt):
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        self.player.audio_set_volume(volume)


    def formatter(self,seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return '{:d}:{:02d}:{:02d}'.format(h, m, s)

class Layers:

    def __init__(self):
        self.tk = tk.Tk()
        self.tk.configure(background = 'black')
        self.tk.update()

        self.bottomFrame = tk.Frame(self.tk, background ='black')
        self.bottomFrame.pack(side =tk.BOTTOM, fill = tk.BOTH, expand = tk.YES)

        self.screen = Screen(self.bottomFrame)
        self.screen.pack(side = tk.TOP)

        self.fullscreen = False
        self.tk.bind("<Key>", self.key)
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)



    def key(self, event):
        pressed = repr(event.char).replace("'", '')
        if pressed == 'p':
            self.screen.pause()
        elif pressed == 'a':
            self.screen.play()
        elif pressed == 's':
            self.screen.stop()

    def toggle_fullscreen(self, event = None):
        self.fullscreen = True
        self.tk.attributes("-fullscreen", self.fullscreen)

    def end_fullscreen(self, event = None):
        self.fullscreen = False
        self.tk.attributes("-fullscreen", self.fullscreen)

class timerThread(Thread):

    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters


if __name__ == '__main__':
    run = Layers()
    run.tk.mainloop()
