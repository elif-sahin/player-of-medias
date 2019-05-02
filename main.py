import tkinter as tk
from tkinter import filedialog
import vlc
import time

class Screen(tk.Frame):
    '''
    Screen widget: Embedded video player from local or youtube
    '''
    def GetHandle(self):
        # Getting frame ID
        return self.winfo_id()

    def chooseFile(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        root.update()
        return file_path

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg = 'black')
        self.settings = { # Inizialazing dictionary settings
            "width" : 1024,
            "height" : 576,
            "o_width":1024,
            "o_height":30,
        }
        self.settings.update(kwargs) # Changing the default settings
        # Open the video source |temporary
        self.video_source = self.chooseFile()

        # Canvas where to draw video output
        self.canvas = tk.Canvas(self, width = self.settings['width'], height = self.settings['height'], bg = "black", highlightthickness = 0)
        self.canvas.pack()

        self.outer_canvas = tk.Canvas(self, width=self.settings['o_width'], height=self.settings['o_height'], bg="white",
                                highlightthickness=0)
        self.outer_canvas.pack()


        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()



        Media = self.instance.media_new(self.video_source)
        Media.get_mrl()
        self.player.set_media(Media)

        # self.player.play()
        self.player.video_set_scale(f_factor=1.5)
        self.player.set_hwnd(self.GetHandle())

        self.var = tk.DoubleVar()
        scale = tk.Scale(self, variable=self.var, orient="horizontal")
        scale.pack()




    def play(self):
        # Function to start player from given source

        self.player.play()


    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()



class Mirror:
    '''
        Mainframe: Display where to put the widgets
    '''
    def __init__(self):
        self.tk = tk.Tk() # Creating the window
        self.tk.configure(background = 'black')
        self.tk.update()

        # Setting up the FRAMES for widgets
        self.bottomFrame = tk.Frame(self.tk, background ='black')
        self.bottomFrame.pack(side =tk.BOTTOM, fill = tk.BOTH, expand = tk.YES)

        # Bindings and fullscreen setting
        self.fullscreen = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        # Screen, BOT
        print("Inizializing Screen...")
        self.screen = Screen(self.bottomFrame)
        self.screen.pack(side = tk.TOP)

        self.tk.bind("<Key>", self.key) # Get inputs from keyboard

    def key(self, event):
        pressed = repr(event.char).replace("'", '')
        if pressed == 'p':
            self.screen.pause()
        elif pressed == 'a':
            self.screen.play()
        elif pressed == 's':
            self.screen.stop()

        else:
            print('fail')

    def toggle_fullscreen(self, event = None):
        self.fullscreen = True
        self.tk.attributes("-fullscreen", self.fullscreen)

    def end_fullscreen(self, event = None):
        self.fullscreen = False
        self.tk.attributes("-fullscreen", self.fullscreen)


if __name__ == '__main__':
    Mir = Mirror()
    #bot = telepot.Bot(TELEGRAM_TOKEN)
    #bot.message_loop(on_chat_message)
    Mir.tk.mainloop()
    #while 1:
        #time.sleep(10)
