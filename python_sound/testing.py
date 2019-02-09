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


def play_clip(file_path, sleep_time=0.05):
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

def play_game_opponent(prevSong, player, error_made, score, round):
    for note in prevSong:
        opponent_note = int(input("Round #{}. {}'s turn: Press a number: ".format(round, player)))

        if note == opponent_note:
            # play the corresponding clip
            play_clip(access_ordered_dict(opponent_note))
            
            score += 1
        else:
            # Play a "mistake" error
            play_clip(base_relative_path + "error.mp3")
            time.sleep(2)

            error_made = True
            print("{}, you made a mistake!".format(player))
            break
            
    return error_made, score
   
        
        
def play_game_composer(song, player, score, round):
    error_made = False
    if round > 1:
        print("-"*20 + " Replay then record new note " + "-"*20)
        error_made, score = play_game_opponent(song, player, error_made, score, round)

    if not error_made:
        print("-"*20 + " Recording " + "-"*20)
        # ask for a key
        key = int(input("Round #{}. {}'s turn: Press a number: ".format(round, player)))
        # play the corresponding clip
        play_clip(access_ordered_dict(key))
        # store clip into a list to record it
        song.append(key)
    return song, error_made, score

def blind_game(name1, name2):
    # Store the round number
    round = 1

    
    # store scores of each player
    score1 = 0
    score2 = 0
    current_score = score1
    # Player name1 starts
    player = name1
    
    error_made = False
    song = []
    while not error_made:
        
        
        # Number of expression per turn is round+3 (so we start at 3 expr)
        print("#"*20 + " Round #{} ".format(round) + "#"*20)
        
        song, error_made, score = play_game_composer(song, player, current_score, round )
        if(error_made):
            break
        current_score = score
        # after a song has been created, opponents needs to repeat it
        
        # change turn
        if player == name1:
            score1 = current_score
            player = name2 
            current_score = score2
        else:
            score2 = current_score
            player = name1
            current_score = score1

        print("-"*20 + " Opponent " + "-"*20)
        
        # increase round number
        round += 1

    # finally say who won and who didn't
    winner = name2 if player == name1 else name1
    winner_score = score1 if winner == name1 else score2
    loser = player
    loser_score = score2 if winner == name1 else score1
    if winner_score == loser_score:
        winner_score = 1
    print("#"*20 + " Results " + "#"*20)
    print("{}, you've Won!\n{}: {}\n{}: {}".format(winner, winner, winner_score, loser, loser_score))



if __name__ == "__main__":
    mixer.init()
    """
    # Play a single clip
    play_clip(audio_clips['sax'])
    """
    # Simulate the game, each key is a facial expression
    blind_game('John', 'Laura')

