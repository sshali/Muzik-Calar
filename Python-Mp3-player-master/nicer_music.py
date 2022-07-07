from tkinter import (
    Tk,HORIZONTAL,Label,Button,
    END,PhotoImage,Scrollbar,Listbox,
    LEFT,StringVar,Menu,Toplevel,
    ACTIVE,BOTH,TOP
    )
from tkinter.filedialog import askdirectory
import pygame
import os
from mutagen.mp3 import MP3
import threading
from tkinter.messagebox import  showerror,askquestion,showinfo
from tkinter import ttk
import time
from PIL import Image,ImageTk

class Player:
    def __init__(self, master):
        self.master = master
        pygame.init()
        pygame.mixer.init()

        #========#
        self.threads = []

        #========#
        def get_icon():
            self.winicon = PhotoImage(file="best (2).png")
            master.iconphoto(False, self.winicon)

        #==========#

        def icon():
            mythreads = threading.Thread(target=get_icon)
            self.threads.append(mythreads)
            mythreads.start()
        icon()

        #=============#

        PLAY = "►"
        PAUSE = "║║"
        RWD = "⏮"
        FWD = "⏭"
        STOP = "■"
        UNPAUSE = "||"
        mute = "🔇"
        unmute = u"\U0001F50A"
        vol_mute = 0.0
        vol_unmute = 1

        #===================#
        self.scroll = Scrollbar(master)
        self.play_list = Listbox(master, font="Sansarif 12 bold", bd=5,
                            bg="white", width=37, height=19, selectbackground="black")
        self.play_list.place(x=600, y=77)
        self.scroll.place(x=946, y=80, height=389, width=15)
        self.scroll.config(command=self.play_list.yview)
        self.play_list.config(yscrollcommand=self.scroll.set)
        
        files = 'best (2).png'
        self.img1 = Image.open(files)
        self.img1 =  self.img1.resize((600, 470), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img1)
        self.lab = Label(master)
        self.lab.grid(row=0, column=0)
        self.lab["compound"] = LEFT
        self.lab["image"] = self.img
     

        #===============#
        self.var = StringVar()
        self.var.set("..............................................................................")
        self.song_title = Label(master, font="Helvetica 12 bold", bg="black",
                        fg="white", width=60, textvariable=self.var)
        self.song_title.place(x=3, y=0)

        # ==========="
    
        def append_listbox():
            global song_list
            try:
                directory = askdirectory()
                os.chdir(directory)
                song_list = os.listdir()
                song_list.reverse()
                for item in song_list:
                    pos = 0
                    self.play_list.insert(pos, item)
                    pos += 1

                global size
                index = 0
                size = len(song_list)
                self.play_list.selection_set(index)
                self.play_list.see(index)
                self.play_list.activate(index)
                self.play_list.selection_anchor(index)
                
            except:
                showerror("Dosya Seçimi Hatası", "Lütfen Dosyayı Doğru Seçin") 
        # =========== #

        def add_songs_playlist():
            mythreads = threading.Thread(target=append_listbox)
            self.threads.append(mythreads)
            mythreads.start()

        #==============#

        def get_time():
            current_time = pygame.mixer.music.get_pos() / 1000
            formated_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
            next_one = self.play_list.curselection()
            song = self.play_list.get(next_one)
            song_timer = MP3(song)
            song_length = int(song_timer.info.length)
            format_for_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            self.label_time.config(text=f"{ format_for_length} / {formated_time}")
            self.progress["maximum"] = song_length
            self.progress["value"] = int(current_time)
            master.after(100, get_time)

        #=========#

        def Play_music():
            try:
                track = self.play_list.get(ACTIVE)
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()
                get_time()
            
                # 
                #
      
            except:
                showerror("Müzik Yok", "Müzik Dİnlemek İstiyorsan Müzik Ekle")

        def playAll():
            try:
                index = 0
                for i in range(size):
                    self.play_list.select_clear(0, END)
                    self.play_list.selection_set(index, last=None)
                    self.play_list.see(index)
                    self.play_list.activate(index)
                    self.play_list.selection_anchor(index)
                    track = self.play_list.get(index)
                    pygame.mixer.music.load(track)
                    self.var.set(track)
                    pygame.mixer.music.play()
                    current_song = self.play_list.curselection()
                    song = self.play_list.get(current_song)
                    song_timer = MP3(song)
                    song_length = int(song_timer.info.length) * 1000
                    get_time()
                    index += 1      
            except:
                showerror("Müzik Playlistte Yok", "Lütfen Müzik EKle")

        def play_all():
            mythreads = threading.Thread(target=playAll)
            self.threads.append(mythreads)
            mythreads.start()
                
        # ===== #

        def pause_unpause():
            if self.button_pause['text'] == PAUSE:
                pygame.mixer.music.pause()
                self.button_pause['text'] = UNPAUSE

            elif self.button_pause['text'] == UNPAUSE:
                pygame.mixer.music.unpause()
                self.button_pause['text'] = PAUSE
    

        # ==== #

        def play_thread():
            mythreads = threading.Thread(target=Play_music)
            self.threads.append(mythreads)
            mythreads.start()

        master.bind("<space>", lambda x: play_thread())

        # ======

        def stop():
            pygame.mixer.music.stop()

        #======#

        def volume(x):
            pygame.mixer.music.set_volume(self.volume_slider.get())

        # ====== #

        def muted():
            if self.button_mute['text'] == unmute:
                pygame.mixer.music.set_volume(vol_mute)
                self.volume_slider.set(vol_mute)
                self.button_mute['fg'] = "red"
                self.button_mute['text'] = mute
            elif self.button_mute['text'] == mute:
                pygame.mixer.music.set_volume(vol_unmute)
                self.volume_slider.set(vol_unmute)
                self.button_mute['fg'] = "white"
                self.button_mute['text'] = unmute

        #======#

        def nextSong():
            try:
                next_one = self.play_list.curselection()
                next_one = next_one[0]+1
                song = self.play_list.get(next_one)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.play_list.select_clear(0, END)
                self.play_list.activate(next_one)
                self.play_list.selection_set(next_one, last=None)
                self.var.set(song)
                get_time()
                self.play_list.see(next_one)
            except:
                showerror("Bundan Sonra Müzik Yok", "Lütfen önceki düğmeye basın")

        def next():
            mythreads = threading.Thread(target=nextSong)
            self.threads.append(mythreads)
            mythreads.start()

        #======#

        def prevSong():
            try:
                next_one = self.play_list.curselection()
                next_one = next_one[0]-1
                song = self.play_list.get(next_one)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.play_list.select_clear(0, END)
                self.play_list.activate(next_one)
                self.play_list.selection_set(next_one, last=None)
                self.var.set(song)
                get_time()
                self.play_list.see(next_one)
            except:
                showerror("Önceki Şarkı yok", "Lütfen İleri düğmesine basın")

        def prev():
            mythreads = threading.Thread(target=prevSong)
            self.threads.append(mythreads)
            mythreads.start()

        self.master.bind('<Left>', lambda x: prev())
        self.master.bind('<Right>', lambda x: next())

        #==========#

        def exit():
            MsgBox = askquestion(
                'Uygulamadan Çık', 'Müzik çalardan çıkmak istediğinizden emin misiniz?.', icon='warning')
            if MsgBox == 'yes':
                master.quit()
                master.after(100, exit)
            else:
                showinfo(
                    'Geri Dön', 'Harika müziğinizi çalmaya devam edin')
            return

        #==========#

        def help():
            top = Toplevel()
            top.title("Help")
            top.geometry("350x554+500+80")
            top.resizable(width=0, height=0)
            user_manual = [
                " MUSIC PLAYER USER MANUAL: \n",
                "1. play button =  ( ► )",
                "2. pause button = ║║ ",
                "3. unpause symbol = ||",
                "4. next button = ⏭ ",
                "5. previous button = ⏮",
                "6. mute button = '\U0001F50A' ",
                "7. unmute symbol = 🔇",
                "8. stop button = ■ ",
                "\n\n| Made by Ali | Copyright @ 2021 |\n"
            ]
            for i in user_manual:
                manual = Label(top, text=i, width=50, height=3,
                            font="Helvetica, 11", bg="black", fg="white")
                manual.pack(side=TOP, fill=BOTH)

        #==============================================================================================#
        #     #
        #===============================================================================================#

        self.menu = Menu(self.lab, font="helvetica, 3",)
        master.config(menu=self.menu)
        self.menu.add_command(label="HELP", command=help)
        self.menu.add_command(label="EXIT", command=exit)

        self.separator = ttk.Separator(self.lab, orient='horizontal')
        self.separator.place(relx=0, rely=0.87, relwidth=1, relheight=1)
        self.button_play = Button(master, text=PLAY, width=5, bd=5, bg="black",
                            fg="white", font="Helvetica, 15", command=play_thread)
        self.button_play.place(x=150, y=415)
        self.button_stop = Button(master, text=STOP, width=5, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=stop)
        self.button_stop.place(x=225, y=415)
        self.button_prev = Button(master, text=FWD, width=5, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=next)
        self.button_prev.place(x=300, y=415)

        self.buttonPlayall = Button(
            self.master, text='\U0001F500' , 
            bg='black', fg='white', font='Helvetica, 15' , bd=5,
            width=3,
            command=play_all)
        self.buttonPlayall.place(x=375, y=415)

        self.button_next = Button(master, text=RWD, width=5, bd=5, bg="black",
                            fg="white", font="Helvetica, 15", command=prev)
        self.button_next.place(x=10, y=415)
        self.button_pause = Button(master, text=PAUSE, width=4, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=pause_unpause)
        self.button_pause.place(x=85, y=415)

        self.button_mute = Button(master, text=unmute, width=2, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=muted)
        self.button_mute.place(x=430, y=415)

        self.label_playlist = Label(master, text=u"♫ Müzik Playlist ♫ ",
                            width=31, font="Helvetica, 15")
        self.label_playlist.place(x=610, y=5)

        self.button_load_music = Button(master, text="♫ Tıkla Ve Müzikleri Yükle ♫", width=43,
                                bd=5, font="Helvetica, 10", bg="black", fg="white", command=add_songs_playlist)
        self.button_load_music.place(x=605, y=45)

        self.style = ttk.Style()

        self.style.configure("myStyle.Horizontal.TScale", background="#505050")

        self.volume_slider = ttk.Scale(self.lab, from_=0, to=1, orient=HORIZONTAL,
                        value=1, length=120, command=volume, style="myStyle.Horizontal.TScale")
        self.volume_slider.place(x=475, y=424)

        self.progress = ttk.Progressbar(self.lab, orient=HORIZONTAL, value=0, length = 453, mode = 'determinate')
        self.progress.place(x=0, y=385)

        self.label_time = Label(master, text="00:00:00 / 00:00:00",
                            width=17, font="Helvetica, 10", bg="black", fg="white")
        self.label_time.place(x=460, y=387)

#=================================Tk==========================================#

def main():
    root = Tk()
    playerapp = Player(root)
    root.geometry("963x470+200+100")
    root.title("Mp3 Müzik Çalar")
    root.configure(bg="black")
    root.resizable(width=0, height=0)
    root.mainloop()

if __name__ == "__main__":
   main()
