import pygame
from pygame import mixer
import numpy as np
from collections import OrderedDict
import time

# Set up a base relative path for all audio clips, use dict to be DRY
base_relative_path = "../sound_clips/"

audio_clips = OrderedDict({
    'sax': base_relative_path + 'alto_sax.wav',
    'drum': base_relative_path + 'basic_drum.wav',
    'funky_guitar': base_relative_path + 'funky_guitar.wav',
    'bass': base_relative_path + 'constant_bass.wav',
    'guitar': base_relative_path + 'guitar_loops.wav'
})


def play_clip(file_path, sleep_time=2):
    """
    Plays a wav file given its relative or absolute path.

    :param file_path: Path of the audio clip.
    :type file_path: str
    :param sleep_time: Number of seconds to sleep for.
    :type sleep_time: int
    :return: Nothing to return
    :rtype: None
    """
    # Load file and play it
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    # Sleeping is needed in order to avoid sound collapsing to 0s. Keep to 2s
    # as this is the length of all the clips, in this way the clips can be
    # played one after the other.
    time.sleep(sleep_time)


def simulate_events():
    """
    Simulates events happening by randomly sampling a time and an integer
    between 0 and 4 (inclusive) to choose a clip to play.
    :return:
    """
    clips = list(audio_clips.items())
    for i in range(10):
        time = np.random.uniform(0, 3)
        instrument = np.random.randint(0, 5)
        play_clip(clips[instrument][1], time)


def access_ordered_dict(index, dictionary=audio_clips):
    """
    Access an ordered dictionary by the specified index.

    :param dictionary:
    :param index:
    :return:
    """
    listed = list(dictionary)
    return dictionary[listed[index]]


def game():
    """
    Simulates the actual game
    :return:
    """
    song = []
    # Keep asking for keys for 10 repetitions
    i = 0
    while i < 10:
        key = input("Press one of 0,1,2,3,4 to generate a sound.\n"
                    "0: Sax\n"
                    "1: Drum\n"
                    "2: Funky Guitar\n"
                    "3: Bass\n"
                    "4: Guitar\n"
                    "Please Press a Key: ")
        key = int(key)
        # Keep prompting user until keys are correct
        while key <0 or key >= 5:
            key = int(input("Key {} not implemented. Try again: ".format(key)))
        # After playing the clip, append it to some list
        play_clip(access_ordered_dict(key))
        song.append(key)
        i += 1
    # When game is finished, play the whole song
    for clip in song:
        play_clip(access_ordered_dict(clip))


if __name__ == "__main__":
    mixer.init()
    """
    # Play a single clip
    play_clip(audio_clips['sax'])
    """
    # Simulate the game, each key is a facial expression
    game()

