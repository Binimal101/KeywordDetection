import pyttsx3
from threading import Thread

class Speech:
    """
    Used to 'bypass' blocking behavior of runAndWait,
    interuption is also a big bonus
    """
    #Initialising pyttsx3 to class
    
    #Need to intsantiate these to be able to use engine loops
    #They never actually get run since we are threading loop calls to the engine
    def onStart(name):
        pass

    def onWord(name, location, length):
        pass

    def onEnd(name, completed):
        if completed:
            engine.stop()
    
    engine = pyttsx3.init()
    engine.connect('started-utterance', onStart)
    engine.connect('started-word', onWord)
    engine.connect('finished-utterance', onEnd)
    engine.setProperty('voice', engine.getProperty('voices')[0].id)

    #Start of class
    
    def __init__(self):
        pass

    #The object itself is callable, but requires the parameter text
    def __call__(text):
        current = Thread(target = Speech.__speak, args = (text,), daemon = True)
        current.start()
        current = None
        
    def __speak(text):
        engine = Speech.engine
        engine.say(text)
        
        try:
            engine.startLoop(True)

        #meaning another thing is in the process of being said
        except RuntimeError: #that or new thing runs and engine loop hasn't stopped yet
            engine.endLoop()
            engine.stop()
            Speech.speak(text)

    def stop():
        say("")

def speak(text):
    Speech.say(text)

def interrupt():
    Speech.stop()
    
