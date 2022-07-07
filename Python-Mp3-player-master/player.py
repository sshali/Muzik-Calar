from tkinter import *
from tkinter.filedialog import askdirectory
import pygame
import os
from mutagen.mp3 import MP3
import threading
from tkinter.messagebox import *
from tkinter import ttk
import time

root = Tk()
root.geometry("865x460+250+100")
root.title("Mp3 Müzik Çalar")
root.configure(bg="black")
root.resizable(width=0, height=0)

#==========#
pygame.init()
pygame.mixer.init()

#============#
threads = []

# =====


def get_icon():
    winicon = PhotoImage(file="best (2).png")
    root.iconphoto(False, winicon)
#==========#


def icon():
    mythreads = threading.Thread(target=get_icon)
    threads.append(mythreads)
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
scroll = Scrollbar(root)
play_list = Listbox(root, font="Sansarif 12 bold", bd=5,
                    bg="white", width=37, height=19, selectbackground="black")
scroll.place(x=850, y=80, height=380, width=15)
play_list.place(x=505, y=77)
scroll.config(command=play_list.yview)
play_list.config(yscrollcommand=scroll.set)

img = PhotoImage(file="best (2).png", width=500, height=460)
lab = Label(root)
lab.grid()
lab["compound"] = LEFT
lab["image"] = img

#===============#
var = StringVar()
var.set("..............................................................................")
song_title = Label(root, font="Helvetica 12 bold", bg="black",
                   fg="white", width=48, textvariable=var)
song_title.place(x=10, y=5)

# ==========="


def append_listbox():
    directory = askdirectory()
    try:
        os.chdir(directory)# 
        song_list = os.listdir()
        song_list.reverse()
        for item in song_list: # 
            pos = 1
            play_list.insert(pos, item)
            pos += 1
    except:
        showerror("Dosya Seçimi Hatası", "Lütfen doğru bir dosya seçin")  
    
# ==========="


def add_songs_playlist():
    mythreads = threading.Thread(target=append_listbox)
    threads.append(mythreads)
    mythreads.start()

#==============#
def get_time():
    global next_one
    current_time = pygame.mixer.music.get_pos() / 1000
    formated_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
    next_one = play_list.curselection()
    song = play_list.get(next_one)
    song_timer = MP3(song)
    song_length = int(song_timer.info.length)
    format_for_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
    label_time.config(text=f"{ format_for_length} / {formated_time}")
    progress["maximum"] = song_length
    progress["value"] = int(current_time)
    root.after(100, get_time)

#=======#


def Play_music():
    try:
        track = play_list.get(ACTIVE)
        pygame.mixer.music.load(play_list.get(ACTIVE))
        var.set(track)
        pygame.mixer.music.play()
        
        get_time()
             
    except:
        showerror("Müzik Yok", "Lütfen çalmak istediğiniz müziği yükleyin")

# =====


def pause_unpause():
    if button_pause['text'] == PAUSE:
        pygame.mixer.music.pause()
        button_pause['text'] = UNPAUSE

    elif button_pause['text'] == UNPAUSE:
        pygame.mixer.music.unpause()
        button_pause['text'] = PAUSE

# ====


def play_thread():
    mythreads = threading.Thread(target=Play_music)
    threads.append(mythreads)
    mythreads.start()
   

# ======

def stop():
    pygame.mixer.music.stop()

#======#

def volume(x):
    pygame.mixer.music.set_volume(slider.get())

# ====

def muted():
    if button_mute['text'] == unmute:
        pygame.mixer.music.set_volume(vol_mute)
        slider.set(vol_mute)
        button_mute['fg'] = "red"
        button_mute['text'] = mute
    elif button_mute['text'] == mute:
        pygame.mixer.music.set_volume(vol_unmute)
        slider.set(vol_unmute)
        button_mute['fg'] = "white"
        button_mute['text'] = unmute

#======#


def nextsong():
    try:
        next_one = play_list.curselection()
        next_one = next_one[0]+1
        song = play_list.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        play_list.select_clear(0, END)
        play_list.activate(next_one)
        play_list.selection_set(next_one, last=None)
        var.set(song)
    except:
        showerror("Bir Sonraki Müzik Yok", "Lütfen önceki düğmeye basın")

#======#


def prev_song():
    try:
        next_one = play_list.curselection()
        next_one = next_one[0]-1
        song = play_list.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        play_list.select_clear(0, END)
        play_list.activate(next_one)
        play_list.selection_set(next_one, last=None)
        var.set(song)
    except:
        showerror("Önceki Müzik Yok", "Lütfen İleri düğmesine basın")

#==========#


def exit():
    MsgBox = askquestion(
        'Uygulamadan Çık', 'Müzik çalardan çıkmak istediğinizden emin misiniz?.', icon='warning')
    if MsgBox == 'yes':
        root.destroy()
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

#==================================================================================================================#
# 
#==================================================================================================================#


menu = Menu(lab, font="helvetica, 3",)
root.config(menu=menu)
menu.add_command(label="Help", command=help)
menu.add_command(label="Exit", command=exit)

separator = ttk.Separator(lab, orient='horizontal')
separator.place(relx=0, rely=0.85, relwidth=1, relheight=1)
button_play = Button(root, text=PLAY, width=5, bd=5, bg="black",
                     fg="white", font="Helvetica, 15", command=play_thread)
button_play.place(x=150, y=407)
button_stop = Button(root, text=STOP, width=5, bd=5,
                     font="Helvetica, 15", bg="black", fg="white", command=stop)
button_stop.place(x=225, y=407)
button_prev = Button(root, text=FWD, width=5, bd=5,
                     font="Helvetica, 15", bg="black", fg="white", command=nextsong)
button_prev.place(x=300, y=407)
button_next = Button(root, text=RWD, width=5, bd=5, bg="black",
                     fg="white", font="Helvetica, 15", command=prev_song)
button_next.place(x=10, y=407)
button_pause = Button(root, text=PAUSE, width=4, bd=5,
                      font="Helvetica, 15", bg="black", fg="white", command=pause_unpause)
button_pause.place(x=85, y=407)
button_mute = Button(root, text=unmute, width=2, bd=5,
                     font="Helvetica, 15", bg="black", fg="white", command=muted)
button_mute.place(x=375, y=407)

label_playlist = Label(root, text=u"♫ Müzik Playlist ♫ ",
                       width=25, font="Helvetica, 15")
label_playlist.place(x=540, y=10)

button_load_music = Button(root, text="♫ Tıkla Ve Müziği Yükle ♫", width=43,
                           bd=5, font="Helvetica, 10", bg="black", fg="white", command=add_songs_playlist)
button_load_music.place(x=505, y=45)

slider = ttk.Scale(lab, from_=0, to=1, orient=HORIZONTAL,
                   value=1, length=80, command=volume)
slider.place(x=415, y=415)

progress = ttk.Progressbar(lab, orient=HORIZONTAL, value=0, length = 350, mode = 'determinate')
progress.place(x=0, y=368)

label_time = Label(root, text="00:00:00 / 00:00:00",
                       width=17, font="Helvetica, 10", bg="black", fg="white")
label_time.place(x=355, y=369)



root.mainloop()

