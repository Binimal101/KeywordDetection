import wave, pyaudio

class waveInterface:
    """
    STATICS ONLY
    Class in which the wave module will be abstracted heavily to do our
    bidding in a neat way. 
    """
    
    def __init__():
        raise Exception("ERROR\nwaveInterface is a static method specific class.")

    def __call__():
        raise Exception("ERROR\nwaveInterface is a static method specific class.")

    
    def readSamples(settings : dict, numFrames):
        
        with wave.open(settings['OUTPUT'], 'rb') as waveFile:
            frameData = waveFile.readframes(numFrames)

            if frameData: #exists
                sampleWidth = waveFile.getsampwidth() #Amount of bytes each sample is represented by
                numSamples = len(frameData) // sampleWidth

                format = {
                    1 : f"{numSamples}b", #Character format
                    2 : f"<{numSamples}h", #Short format
                    4 : f"<{numSamples}l", #Long format
                }[sampleWidth]
		
                return struct.unpack(format, frameData) #Integer format of each frame
            else:
                return []

    @staticmethod
    def writeAudioToFile(settings : dict, output, samples):
        p = pyaudio.PyAudio()
        wf = wave.open(settings['OUTPUT'], 'wb')
        wf.setnchannels(settings['CHANNELS'])
        wf.setsampwidth(p.get_sample_size(settings['FORMAT']))
        wf.setframerate(settings['RATE'])
        wf.writeframes(b''.join(frames))
        wf.close()


class Listener:
    def __init__(self, outputFile):
        if not outputFile.endswith(".wav"):
            changeToWav(outputFile)
            #raise Exception("ERROR\nthe selected output file for Listener instance isn't a .WAV")
        self.audioSettings = {
            "OUTPUT" : outputFile,
            "CHUNK" : 1024,
            "FORMAT" : pyaudio.paInt8, #1 byte wide samples
            "CHANNELS" : 1, #Mono audio input
            "RATE" : 44100 #Samples collected per second, 44100 is pretty standardized
            
        }
