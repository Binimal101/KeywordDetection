import speech_recognition as sr
import os, math

import pyaudio
import wave
import sys

CHUNK = 1024 #Number of frames a signal is split into
FORMAT = pyaudio.paInt8 # 2byte sample size * 44100 samples a second seems decent
CHANNELS = 1 # each frame contains x sound samples
RATE = 44100 #Frames collected per second
RECORD_SECONDS = 15 #we can fix this later since we actually want continuous audio recording
WAVE_OUTPUT_FILENAME = "threePauses.wav"

"""
Questions and concerns:
- How do we check for quiet frames? Measure amplitudes and check for x percent difference over y seconds
- How do we check for wake words?
    - Most likely will have to save current frames to a file and test that in recognizer
- Why isn't recognizer working
"""

def recordAudio():
    p = pyaudio.PyAudio()

    input_ = True
    stream = p.open(format=FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = input_,
            output= not input_,
            frames_per_buffer = CHUNK)

    stream.start_stream()

    quietFrames = 0 
    keyword = False
    testForKeyword = lambda: None

    frames = []
    
    #Measuring audio
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): 
        data = stream.read(CHUNK)
        frames.append(data)
        
        if i % RATE == 0: #every second test current frames for wake word
            testForKeyword()

        #if we get 3 seconds worth of quiet frames after keyword, return frames
        if (quietFrames >= int((RATE/CHUNK)) * 3) and keyword: #RATE/CHUNK frames per second
            break

    stream.stop_stream()
    stream.close()

    p.terminate()
    return frames

def playAudio(frames):
    play=pyaudio.PyAudio()
    stream_play=play.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          output=True)
    for data in frames: 
        stream_play.write(data)
        
    stream_play.stop_stream()
    stream_play.close()
    play.terminate()

def writeAudioToFile(frames):
    p = pyaudio.PyAudio()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def getTextFromAudio(frames):
    audio = sr.AudioFile(b''.join(frames))
    
print(f"Recording for {RECORD_SECONDS} seconds...")
frames = recordAudio()
print("Recording finished\nPlaying audio...")
playAudio(frames)
print("Writing data to file...")
writeAudioToFile(frames)
print("Done!")
#print(getTextFromAudio(frames))
