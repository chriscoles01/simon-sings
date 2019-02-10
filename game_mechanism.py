import pygame
from pygame import mixer
import numpy as np
from collections import OrderedDict
import time
import zmq
from lib.facial_expressions import FacialExpressionDetector

# Set up a base relative path for all audio clips, use dict to be DRY
base_relative_path = "sound_clips/"

audio_clips = OrderedDict({
    'sax': base_relative_path + 'alto_sax.wav',
    'drum': base_relative_path + 'basic_drum.wav',
    'funky_guitar': base_relative_path + 'funky_guitar.wav',
    'bass': base_relative_path + 'constant_bass.wav',
    'guitar': base_relative_path + 'guitar_loops.wav'
})

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

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


def access_ordered_dict(index, dictionary=audio_clips):
    """
    Access an ordered dictionary by the specified index.

    :param dictionary:
    :param index:
    :return:
    """
    listed = list(dictionary)
    return dictionary[listed[index]]


def play_game_opponent(prevSong, player, error_made, score, thread):
    """
    Loops through all clips in the song and requests an expression, which is
    then converted to a clip. If the clip in the song is the same of the clip
    identified by the facial expression, we increase the score. Otherwise, we
    produce an error sound.

    :param prevSong: List of clips from previous round.
    :type prevSong: list
    :param player: Name/index of the player. To be used by OpenCV stuff. Should
                   be a string of an integer (either '0' or '1').
    :type player: str
    :param error_made: Whether player has played a different note.
    :type error_made: bool
    :param score: Current score of player.
    :type score: int
    :param thread: Current Thread
    :type thread: Thread
    :return: error_made, score
    :rtype: tuple
    """
    for note in prevSong:
        opponent_note = convert_expression(thread.get_expression(int(player)))

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
   

def play_game_composer(song, player, score, round, thread):
    """
    Handles the two main situations of a player: repeating the previous song
    and recording a new sound.

    :param song: Previous song. It consists of all the sound clips used before.
    :type song: list
    :param player: Name/index of the player. To be used by OpenCV stuff. Should
                   be a string of an integer (either '0' or '1').
    :type player: str
    :param score: Current score of the game for this player.
    :type score: int
    :param round: Number of round we are in.
    :type round: int
    :param thread: Current thread.
    :type thread: Thread
    :return: song, error_made, score
    :rtype: tuple
    """
    error_made = False
    if round > 1:
        print("-"*20 + " Replay then record new note " + "-"*20)
        error_made, score = play_game_opponent(song, player, error_made,
                                               score, thread)

    if not error_made:
        print("-"*20 + " Recording " + "-"*20)
        # ask for a key
        key = convert_expression(thread.get_expression(int(player)))
        # play the corresponding clip
        play_clip(access_ordered_dict(key))
        # store clip into a list to record it
        song.append(key)
    return song, error_made, score


def convert_expression(expression):
    """
    Converts facial expressions to integer encoding so we can use game
    mechanics.

    :param expression: Facial expression.
    :type expression: str
    :return: Integer encoding
    :rtype: int
    """
    if expression == "smiling": 
        return 0
    elif expression == "opened-mouth":
        return 1
    elif expression == "frowning":
        return 2



from flask import Flask, render_template, Response
from lib.facial_expressions import VideoCamera

vc = VideoCamera()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



from multiprocessing.connection import Client

address = ('127.0.0.1', 6000)
conn = Client(address)





def blind_game(name1, name2, thread):
    print("[INFO] Started game")
    """
    Plays the actual game.

    :param name1: Name / index of player1.
    :param name2: Name / index of player2.
    :param thread: Current thread.
    :return: Nothing to return.
    :type: None
    """
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
	
	first_req = socket.recv()
	
    while not error_made:

        conn.send(gen(vc))

        # Number of expression per turn is round+3 (so we start at 3 expr)
        print("#"*20 + " Round #{} ".format(round) + "#"*20)
        
        song, error_made, score = play_game_composer(
            song, player, current_score, round, thread
        )
        if error_made:
            break
        current_score = score
        
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
    conn.close()

    # finally say who won and who didn't
    winner = name2 if player == name1 else name1
    winner_score = score1 if winner == name1 else score2
    loser = player
    loser_score = score2 if winner == name1 else score1
    if winner_score == loser_score:
        winner_score = 1
    print("#"*20 + " Results " + "#"*20)
    print("{wname}, you've Won!\n{wname}: {wscore}\n{lname}: {lscore}"
          .format(wname=winner, wscore=winner_score,
                  lname=loser, lscore=loser_score))











if __name__ == "__main__":
    mixer.init()


    # Create new threads
    # thread1 = FacialExpressionDetector(1, "Facial-Thread")
    # # Start new Threads
    # thread1.start()
    # Simulate the game, each key is a facial expression

    blind_game('0', '1', vc.thread1) 
