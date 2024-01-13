from datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# Speech engine  initialisation
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # 0 = male, 1= female
activationWord = 'computer' # Single word

# Configure browser
# set the path
chrome_path = r"c:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# wolfram Alpha client
appId = '5R4937-J888YX9J2V'
wolframClient = wolframalpha.Client(appId)
def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)


    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print("I don't understand that please try again")
        speak("I don't understand that please try again")
        print(exception)
        return 'None'

    return query

def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No Wikipedia result')
        return 'No result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']


def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)

    if response['@success'] == 'false':
        return 'Could not compute'

    else:
        result = ''

        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):

            result = listOrDict(pod1['subpod'])

            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            return question.split('(')[0]
            speak('Computation failed. Querying universal databank.')
            return search_wikipedia(question)


# Main loop
if __name__== '__main__':
    speak('All system nominal .')

    while True:
        # Parse  as a list
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            # List commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all.')
                else:
                    query.pop(0) # Remove say
                    speech = ' '.join(query)
                    speak(speech)


            # Navigation
            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            # Wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying the universal databank.')
                speak(search_wikipedia(query))

            # wolfram Alpha
            if query[0] == 'computer' or query[0] == 'computer':
                query = ' '.join(query[1:])
                speak('Computing')
                try:
                    result = search_wolframAlpha(query)
                    speak(result)
                except:
                    speak('Unable to compute.')

            if query[0] == 'log':
                speak('Ready to record your note')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

                with open('note_%S.txt', 'w') as newFile:
                    newFile.write(newNote)
                speak('Note written')

            if query[0] == 'exit':
                speak('Goodbye')
                break