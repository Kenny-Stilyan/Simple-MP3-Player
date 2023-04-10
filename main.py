import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import pygame

root = tk.Tk()
root.title("MP3 Player!")
root.iconbitmap("icon.ico")
root.geometry("620x325")

songs = {}

def add_song_to_list(song):
    if song:
        song_name = song
        song_name = song_name.split("/")[-1] # get the name of the file only
        song_name = song_name.replace(".mp3", "")
        song_list_box.insert(END, song_name)
        songs[song_name] = song


# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir="C:/Users/YourName/Desktop/MyMusic", title="Choose a Song", filetypes=(("MP3 Files", "*.mp3"),))
    add_song_to_list(song)

# Add Many Song Function
def add_many_songs():
    songs = filedialog.askopenfilename(initialdir="C:/Users/YourName/Desktop/MyMusic", title="Choose Songs", filetypes=(("MP3 Files", "*.mp3"),), multiple=True)
    # Loop Thru Song List And Replace Directory Info & .mp3
    for song in songs:
        add_song_to_list(song)

# Play Selected Song
def play():
    song = song_list_box.get(ACTIVE)
    pygame.mixer.music.load(songs[song])
    pygame.mixer.music.play(loops=0)


# Stop Playing Current Song
def stop():
    pygame.mixer.music.stop()
    song_list_box.select_clear(ACTIVE)

# Pause & Unpase Current Song
paused = False
def pause():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


# Create Playlist
song_list_box = tk.Listbox(root, background="black", foreground="white", selectbackground="gray", selectforeground="cyan", width=60)
song_list_box.pack(pady=20)

# Initialize pygame mixer
pygame.mixer.init()

# Defining Buttons Player Controls
back_button_image =    Image.open("Button images/back_button.png").resize((100, 100), Image.ANTIALIAS)
back_button_photo =    ImageTk.PhotoImage(back_button_image)

forward_button_image = Image.open("Button images/forward_button.png").resize((100, 100), Image.ANTIALIAS)
forward_button_photo = ImageTk.PhotoImage(forward_button_image)

play_button_image =    Image.open("Button images/play_button.png").resize((100, 100), Image.ANTIALIAS)
play_button_photo =    ImageTk.PhotoImage(play_button_image)

pause_button_image =   Image.open("Button images/pause_button.png").resize((100, 100), Image.ANTIALIAS)
pause_button_photo =   ImageTk.PhotoImage(pause_button_image)

stop_button_image =   Image.open("Button images/stop_button.png").resize((100, 100), Image.ANTIALIAS)
stop_button_photo =   ImageTk.PhotoImage(stop_button_image)

# Player Control Button Images Frame
controls_frame = Frame(root)
controls_frame.pack()

# Player Control Button Images
back_button =    Button(controls_frame, image=back_button_photo,    borderwidth=0, width=100, height=100)
forward_button = Button(controls_frame, image=forward_button_photo, borderwidth=0, width=100, height=100)
play_button =    Button(controls_frame, image=play_button_photo,    borderwidth=0, width=100, height=100, command=play)
pause_button =   Button(controls_frame, image=pause_button_photo,   borderwidth=0, width=100, height=100, command=pause)
stop_button =    Button(controls_frame, image=stop_button_photo,    borderwidth=0, width=100, height=100, command=stop)

back_button.grid   (row=0, column=0, padx=10)
forward_button.grid(row=0, column=4, padx=10)
play_button.grid   (row=0, column=2, padx=10)
pause_button.grid  (row=0, column=3, padx=10)
stop_button.grid   (row=0, column=1, padx=10)

# Menu
my_menu = Menu()
root.config(menu=my_menu)

# Add Songs To Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)

# Add Many Songs To Menu
add_song_menu.add_command(label="Add Many Song to Playlist", command=add_many_songs)





root.mainloop()
