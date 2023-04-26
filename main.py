import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
import pygame
import time

root = tk.Tk()
root.title("MP3 Player!")
root.iconbitmap("Simple MP3 player/icon.ico")
root.geometry("620x500")

songs = {}

def add_song_to_list(song):
    if song:
        song_name = song
        song_name = song_name.split("/")[-1] # get the name of the file only
        song_name = song_name.replace(".mp3", "")
        song_list_box.insert(END, song_name)
        songs[song_name] = song


# Song Lenght (Time)
def song_lenght():
    current_time = pygame.mixer.music.get_pos() / 1000
    # Get Data Lable
    slider_lable.config(text=f'Slider: {int(music_slider.get())} and Song Position: {int(current_time)}')

    converted_time = time.strftime("%H:%M:%S", time.gmtime(current_time))

    # Get Song Lenght wight Mutagen.mp3
    # Get Current Song
    song = song_list_box.get(ACTIVE)
    song = songs[song]
    song_mutagen = MP3(song)
    global song_lenght_mutagen
    song_lenght_mutagen = song_mutagen.info.length
    converted_song_lenght = time.strftime("%H:%M:%S", time.gmtime(song_lenght_mutagen))

    current_time += 1
    if int(music_slider.get()) == int(song_lenght_mutagen):
        status_bar.config(text=f"Time: {converted_song_lenght}/{converted_song_lenght}  ")
    elif int(music_slider.get()) == int(current_time):
        # Slider hasn't been moved
        # Update Slider
        slider_lenght = int(song_lenght_mutagen)
        music_slider.config(to=slider_lenght, value=current_time)
    else:
        # Slider has been moved
        # Update Slider
        slider_lenght = int(song_lenght_mutagen)
        music_slider.config(to=slider_lenght, value=music_slider.get())

        converted_song_lenght = time.strftime("%H:%M:%S", time.gmtime(int(music_slider.get())))
        status_bar.config(text=f"Time: {converted_time}/{converted_song_lenght}  ")

        passing_time = int(music_slider.get()) + 1
        music_slider.configure(value=passing_time)

    # Update Time
    status_bar.after(1000, song_lenght)

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

# Remove a Song
def remove_song():
    song_list_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# Remove All Songs
def remove_all_songs():
    song_list_box.delete(0, END)
    pygame.mixer.music.stop()


# Play Selected Song
def play():
    song = song_list_box.get(ACTIVE)
    pygame.mixer.music.load(songs[song])
    pygame.mixer.music.play(loops=0)
    # Calling Song Lenght (Time)
    song_lenght()

# Stop Playing Current Song
def stop():
    pygame.mixer.music.stop()
    song_list_box.select_clear(ACTIVE)
    # Remove Song Lenght Text
    status_bar.config(text="")

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

# Play the Next Song In PlayList
def next():
    # Current Song NUM
    next_one = song_list_box.curselection()
    # Adding one to the Current Song NUM
    next_one = next_one[0]+1
    song = song_list_box.get(next_one)
    
    pygame.mixer.music.load(songs[song])
    pygame.mixer.music.play(loops=0)

    song_list_box.selection_clear(0, END)
    song_list_box.activate(next_one)
    song_list_box.select_set(next_one, last=None)

# Play the Previous Song In PlayList
def back():
    # Current Song NUM
    previous_one = song_list_box.curselection()
    # Subtraction one to the Current Song NUM
    previous_one = previous_one[0]-1
    song = song_list_box.get(previous_one)
    
    pygame.mixer.music.load(songs[song])
    pygame.mixer.music.play(loops=0)

    song_list_box.selection_clear(0, END)
    song_list_box.activate(previous_one)
    song_list_box.select_set(previous_one, last=None)

# Slider Function
def slide(x):
    slider_lable.config(text=f'{int(music_slider.get())} of {int(song_lenght_mutagen)}')


# Create Playlist
song_list_box = tk.Listbox(root, background="black", foreground="white", selectbackground="gray", selectforeground="cyan", width=60)
song_list_box.pack(pady=20)

# Initialize pygame mixer
pygame.mixer.init()

# Defining Buttons Player Controls
back_button_image =    Image.open("Simple MP3 player/Button images/back_button.png").resize((100, 100), Image.ANTIALIAS)
back_button_photo =    ImageTk.PhotoImage(back_button_image)

forward_button_image = Image.open("Simple MP3 player/Button images/forward_button.png").resize((100, 100), Image.ANTIALIAS)
forward_button_photo = ImageTk.PhotoImage(forward_button_image)

play_button_image =    Image.open("Simple MP3 player/Button images/play_button.png").resize((100, 100), Image.ANTIALIAS)
play_button_photo =    ImageTk.PhotoImage(play_button_image)

pause_button_image =   Image.open("Simple MP3 player/Button images/pause_button.png").resize((100, 100), Image.ANTIALIAS)
pause_button_photo =   ImageTk.PhotoImage(pause_button_image)

stop_button_image =    Image.open("Simple MP3 player/Button images/stop_button.png").resize((100, 100), Image.ANTIALIAS)
stop_button_photo =    ImageTk.PhotoImage(stop_button_image)

# Create a frame for the slider and buttons
slider_frame = tk.Frame(root)
slider_frame.pack(pady=10)

# Create the slider
music_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=400, command=slide)
music_slider.grid(row=0, column=0, pady=5)

# Create the slider label
slider_lable = tk.Label(slider_frame, text='0')
slider_lable.grid(row=1, column=0)

# Player Control Button Images Frame
controls_frame = Frame(root)
controls_frame.pack(pady=10)

# Player Control Button Images
back_button =    Button(controls_frame, image=back_button_photo,    borderwidth=0, width=100, height=100, command=back)
forward_button = Button(controls_frame, image=forward_button_photo, borderwidth=0, width=100, height=100, command=next)
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

# Add Songs To Menu & Add Many Songs To Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
add_song_menu.add_command(label="Add Many Song to Playlist", command=add_many_songs)

# Delete Songs To Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Song", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove Selected Playing Song From Playlist", command=remove_song)
remove_song_menu.add_command(label="Remove All Songs From Playlist", command=remove_all_songs)

# Create Status Bar
status_bar = Label(root, text="", border=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)




root.mainloop()
