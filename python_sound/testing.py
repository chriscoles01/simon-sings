import pygame
from pygame import mixer
import time


def play_clip(file_path):
    """
    Plays a wav file given its relative or absolute path.

    :param file_path: Path of the audio clip.
    :type file_path: str
    :return: Nothing to return
    :rtype: None
    """
    # Load file and play it
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    # Sleeping is needed in order to avoid sound collapsing to 0s. Keep to 2s
    # as this is the length of all the clips, in this way the clips can be
    # played one after the other.
    time.sleep(2)


if __name__ == "__main__":
    mixer.init()
    play_clip("../sound_clips/alto_sax.wav")
    play_clip("../sound_clips/basic_drum.wav")
    play_clip("../sound_clips/funky_guitar.wav")