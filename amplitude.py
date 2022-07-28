import wave, struct

"""
Given a wave file, will return average amplitude values as a list of length x
where x is the length of the wave file in seconds.
"""

filename = ""

def readSamples(waveFile, numFrames):
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

def roundReadableAmplitudes(amplitudes): #edits input, doesn't return BAD PRACTICE
	for amplitudeIndex in range(len(amplitudes)):
		amplitudes[amplitudeIndex] = round(amplitudes[amplitudesIndex], 4)
		
#make way to find averages of non-static times, like 0.5 sec or 0.1 instead of hardcoding
def getAveragedAmplitudes(filename):	
	with wave.open(filename, "rb") as wavefile:
		frameCount = wavefile.getnframes()
		
		samplesPS = wavefile.getframerate()
		sampleData = readSamples(wavefile, frameCount)
		seconds = len(sampleData) // samplesPS #Average every second worth of data
	
		averagedAmplitudes = []
		average = lambda x: sum(x) / len(x)
		
		#Counteracts false quiet sections, when in reality just different amplitude signs (+ vs -)
		absAll = lambda secondSampleCollection: tuple(map(lambda sample: abs(sample), secondSampleCollection))
		for second in range(1, seconds+1, 1):
			#lastSecondLastSample : CurrentSecondLastSample
			secondSampleCollection = absAll(sampleData[((second-1) * samplesPS) : (second * samplesPS)]) #Make all amplitudes positive for current second
			averagedAmplitudes.append(average(secondSampleCollection))
		
		#gets rest of samples that don't fit in 1 second splittings and appends
		averagedAmplitudes.append(
			average(
				absAll(sampleData[(seconds * samplesPS):]) #fixes amplitudes
			)
		)
		
	return averagedAmplitudes

amps = getAveragedAmplitudes(filename)
print(amps)
