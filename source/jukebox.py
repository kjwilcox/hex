#
# Copyright (c) 2008 Kyle J. Wilcox
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
jukebox.py
A simple and convenient abstraction of the PyGame sound system.

This jukebox has three primary functions:
- semi-automatic music loading
- easy sound effect use
- easy background music

To use, simply import the module, and call jukebox.sound (with
an optional directory name) to get a reference to the jukebox.

It might be handy to store the reference locally:
import jukebox
music = jukebox.sound()

Play sound effects like so:
jukebox.sound()["explosion"].play()

Play background music like so:
jukebox.sound().play_music()

Make *absolutely* sure that you call:
jukebox.sound().stop_music()
otherwise, your program may not end!
"""


import pygame

import threading
import random
import copy
import glob
import os

__jukebox = None

def sound(directory="sounds"):
    """
    Returns a singleton Jukebox instance.
    """
    
    global __jukebox
    
    if not __jukebox:
        __jukebox = Jukebox(directory)
        
    return __jukebox


class Jukebox(object):
    def __init__(self, autoload="sounds"):
        if not pygame.mixer.get_init():
            pygame.mixer.init()        
        self.songs = {}
        self.channels = {}
        
        self.music = []
        self.music_queue = []
        self.music_playing = False

        if autoload:
            self.auto_load(autoload)

    def auto_load(self, directory="sounds"):
        """ Automatically loads all sounds in the given subdirectory. """
        
        songs = []
        # sounds
        for song in glob.glob(os.path.join(directory, "*.wav")):
            songs.append(song)

        for song in glob.glob(os.path.join(directory, "*.ogg")):
            songs.append(song)
        
        for song in songs:
            self.load(song.split('.')[0].split(os.path.sep)[1], song)

        songs = []
        # background music
        for song in glob.glob(os.path.join(directory, "music", "*.wav")):
            self.music.append(song)

        for song in glob.glob(os.path.join(directory, "music", "*.ogg")):
            self.music.append(song)

    def load(self, name, filename):
        """ Loads a song into the jukebox. """
        sound = pygame.mixer.Sound(filename)
        self.songs[name] = sound

    def play(self, name):
        """ Plays a song once in a dedicated channel. """
        self.channels[name] = self.songs[name].play()

    def stop(self, name):
        """ Stops the specified song. """
        self.songs[name].stop()

    def pause(self, name):
        """ Pauses the specified song. """
        self.channels[name].pause()

    def unpause(self, name):
        """ Unpauses the specified song. """
        self.channels[name].unpause()

    def fadeout(self, name, time):
        """ Fades out the specified song over given milliseconds. """
        self.channels[name].fadeout(time)

    def load_music(self, filename):
        """ Loads a filename into the music listing. """
        self.music.append(filename)

    def play_music(self):
        """ Starts the music playing """

        self.music_playing = True
        self.music_thread = JukeboxContinuous(self)
        self.music_thread.start()

    def stop_music(self):
        """ Stops the background music. """
        self.music_playing = False
        pygame.mixer.stop()

    def update_music(self):
        """
        Needs to be called in most loops to ensure continuous background music.
        Will randomly pick a new song to play in the background after the
        last one finishes.
        """

        # immediately break if we are playing something
        if pygame.mixer.get_busy():
            return

        # throw a warning if there isn't any music
        if not self.music:
            print("no music loaded")
            return

        # fill up the queue with songs
        if not self.music_queue:
            self.music_queue = copy.copy(self.music)
            random.shuffle(self.music_queue)

        # loads a random music song from the queue and plays it
        song = self.music_queue.pop()
        self.mixer_song = pygame.mixer.Sound(song)
        #print("now playing:", song.split(os.path.sep)[-1])
        self.mixer_song.play()


    def fadeout_music(self, time):
        """ Fades out the background music over given milliseconds. """
        pygame.mixer.music.fadeout(time)


class JukeboxContinuous(threading.Thread):
    """ A thread to keep the background music playing. """

    def __init__(self, target):
        """ We need to pass in the jukebox that we will be messing with. """
        self.target = target
        threading.Thread.__init__(self)

    def run(self):
        """ Calls the code to make sure music is playing. """

        while self.target.music_playing:
            self.target.update_music()
            pygame.time.wait(250)
            

    
