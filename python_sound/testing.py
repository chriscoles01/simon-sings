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


def play_clip(file_path, sleep_time=1):
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


def game_with_turns(name1, name2):
    """
    Simulates the game with turns.
    :param name1: Name of player 1
    :type name1: str
    :param name2: Name of player 2
    :type name2: str
    :return: Nothing to return
    :rtype: None
    """
    song = []
    # Keep asking for keys for 10 repetitions
    i = 0
    turn = True  # True corresponds to name1
    while i < 10:
        # decide the person's name based on True/False
        player = name1 if turn else name2
        key = input("Round #{}. {}'s turn. Press one of 0,1,2,3,4 to generate"
                    " a sound.\n"
                    "0: Sax\n"
                    "1: Drum\n"
                    "2: Funky Guitar\n"
                    "3: Bass\n"
                    "4: Guitar\n"
                    "Please Press a Key: ".format(i+1 % 2, player))
        key = int(key)
        # Keep prompting user until keys are correct
        while key <0 or key >= 5:
            key = int(input("Key {} not implemented. Try again: ".format(key)))
        # After playing the clip, append it to some list
        play_clip(access_ordered_dict(key))
        song.append(key)
        i += 1
        # finally change the turn
        turn = ~turn
    # When game is finished, play the whole song
    for clip in song:
        play_clip(access_ordered_dict(clip))


def blind_game(name1, name2):
    # Store the round number
    round = 0
    # number of initial expressions - 3
    n_expr = 1
    # store scores of each player
    score1 = 0
    score2 = 0
    # Player name1 starts
    player = name1
    # Game stops when a player makes 3 or more consecutive errors
    errors1 = 0
    errors2 = 0
    while errors1 < 3 and errors2 < 3:
        song = []
        # Number of expression per turn is round+3 (so we start at 3 expr)
        while n_expr <= round+3:
            # ask for a key
            key = int(input("Round #{}. Recording. {}'s turn: Press a number: ".format(round+1, player)))
            # play the corresponding clip
            play_clip(access_ordered_dict(key))
            # store clip into a list to record it
            song.append(key)
            # increase expression number
            n_expr += 1
        # after a song has been created, opponents needs to repeat it
        # change turn
        player = name2 if player == name1 else name1
        for index, clip in enumerate(song):
            key = int(input("Round #{}. Opponent. {}'s turn: Press a number: ".format(round+1, player)))
            # play the corresponding clip
            play_clip(access_ordered_dict(key))
            # compare this with the key used by same player
            if key == song[index]:
                # clip is correct, increase score of opponent
                score1 = score1 + 1 if player == name1 else score1
                score2 = score2 + 1 if player == name2 else score2
                # when player is correct, reset the errors if he's not reached 3 yet
                if player == name1 and errors1 < 3:
                    errors1 = 0
                elif player == name2 and errors2 < 3:
                    errors2 = 0
            else:
                # increase counter of errors
                errors1 = errors1 + 1 if player == name1 else errors1
                errors2 = errors2 + 1 if player == name2 else errors2
                # print an error message
                error = errors2 if player == name2 else errors1
                print("{}, you made a mistake! Cumulative error: {}".format(player, error))
        # increase round number
        round += 1
        # reset the number of expressions
        n_expr = 1
        # reset the song
        song = []
    # finally say who won and who didn't
    winner = name2 if player == name1 else name1
    winner_score = score1 if winner == name1 else score2
    loser = player
    loser_score = score2 if winner == name1 else score1
    print("#"*80)
    print("{}, you've Won!\n{}: {}\n{}: {}".format(winner, winner, winner_score, loser, loser_score))


if __name__ == "__main__":
    mixer.init()
    """
    # Play a single clip
    play_clip(audio_clips['sax'])
    """
    # Simulate the game, each key is a facial expression
    blind_game('John', 'Laura')

