from gtts import gTTS
import vlc
import time
import os
import random

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

words = []

with open('words.txt','r') as file:
    for line in file:
        line = line.strip('\n')
        words.append(line)

if not os.path.exists('_output'):
   os.makedirs('_output')

current_working_directory = os.getcwd()
getch = _Getch()

print('Repeat the word using the talon alphabet, say "bang bang" to exit')

while True:
    word_input = ''
    index = random.randint(0,len(words))
    correct_word = words[index]

    tts = gTTS(correct_word, lang='en', tld='us')
    tts.save('_output/output.mp3')
    p = vlc.MediaPlayer(f"file://{current_working_directory}/_output/output.mp3")
    p.play()

    while (word_input != correct_word) and (len(word_input) < len(correct_word)):
        x = getch()
        word_input += x
        if word_input == '!!':
            exit(0)
        elif word_input != '!' and correct_word[:len(word_input)] != word_input:
            break
    if word_input == correct_word:
        print(f'"{correct_word}" is correct!')
    else:
        print(f'Fail! "{word_input}" is not equal to "{correct_word}"!')
