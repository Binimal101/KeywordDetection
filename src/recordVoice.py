#Built-In
import sys, os, math

#File Imports
import speech

#Natives
import speech_recognition as sr
import pyaudio, wave

CHUNK = 1024 #Number of frames a signal is split into
FORMAT = pyaudio.paInt8 # 2byte sample size * 44100 samples a second seems decent
CHANNELS = 1 # each frame contains x sound samples
RATE = 44100 #Samples collected per second
RECORD_SECONDS = 15 #we can fix this later since we actually want continuous audio recording
WAVE_OUTPUT_FILENAME = "noticablePauses.wav"

def recordAudio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            output= False,
            frames_per_buffer = CHUNK)

    stream.start_stream()

    quietFrames = 0 
    keyword = False
    testForKeyword = lambda: None

    frames = []
    
    #Measuring audio
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #important stuff
        data = stream.read(CHUNK)
        frames.append(data)

        #pseudo code
        if i % RATE == 0: #every second test current frames for wake word
            testForKeyword()

        #pseudo code
        #if we get 3 seconds worth of quiet frames after keyword, return frames
        if (quietFrames >= RATE * 3) and keyword:
            break

    stream.stop_stream()
    stream.close()

    p.terminate()
    return frames

def playAudio(frames):
    play=pyaudio.PyAudio()

    stream_play=play.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True #Denotes 
    )
    
    for data in frames: 
        stream_play.write(data)
        
    stream_play.stop_stream()
    stream_play.close()
    play.terminate()

def writeAudioToFile(frames):
    p = pyaudio.PyAudio()
    
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
print(f"Recording for {RECORD_SECONDS} seconds...")
frames = recordAudio()
print("Recording finished\nPlaying audio...")
playAudio(frames)
print("Writing data to file...")
writeAudioToFile(frames)
print(f"Done!\nFile saved as {WAVE_OUTPUT_FILENAME}")
