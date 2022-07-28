 - Listener will need run in a different process (Multiprocessing)
 - Listener needs to be able to record and recognize audio in the same process, listener recording needs to be non-blocking (PyAudio callback mode) \[https://stackoverflow.com/questions/62618934/pyaudio-how-to-access-stream-read-data-in-callback-non-blocking-mode]
 - Listener should flag when a keyword has been called and then record until silence, restarting itself and returning the text representation of the audio when silence is apparent.


KEYWORD RECOGNITION:

Audio recognition should be snappy, but cannot involve homemade AI we can use existing modules like SpeechRecognition, testing x second clips for keywords every y seconds as to be non-blocking. These clips should be recent, to do this, we can remove x frames/samples from the front of the list of audio data and add x frames to the front.


COMMAND START/STOP:

start:
 - When a keyword is tested and flagged, we can start concatenating recognised words onto a string until silence breaks the listening process

stop:
 - Every audio frame/sample contains the recorded amplitude of the wave signature at the current time, meaning that if we test for lower than average    amplitudes, we can detect silent frames with some manipulation. 
 - After x seconds of silent frames from there we should be able to reset flag and wait for all outgoing SpeechRecognition requests are done, then continue listening.
