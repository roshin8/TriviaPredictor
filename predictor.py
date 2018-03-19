import requests
import pyscreenshot as Imagegrab
from base64 import b64encode
import json
import io
import webbrowser

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate';
API_KEY = '' # Use your API Key

# List of words to clean from the question during google search
WORDS_TO_STRIP = [
    'who', 'what', 'where', 'when', 'of', 'and', 'that', 'have', 'for',
    'on', 'with', 'as', 'this', 'by', 'from', 'they', 'a', 'an', 'and', 'my',
    'in', 'to', '?', ',', 'these', 'which'
]

def get_question():
    buffer = io.BytesIO()
    Imagegrab.grab(bbox=(42, 373, 335, 685)).save(buffer, format='PNG')  # Mob Show
    # Imagegrab.grab(bbox=(18, 238, 352, 546)).save(buffer, format='PNG')  # BrainBaazi
    # Imagegrab.grab(bbox=(18, 238, 352, 546)).save(buffer, format='PNG')  # Loco

    ctxt = b64encode(buffer.getvalue()).decode()
    img_requests = {
        'image': {'content': ctxt},
        'features': [{
            'type': 'DOCUMENT_TEXT_DETECTION',
            'maxResults': 2
        }]
    }

    image_data = json.dumps({"requests": img_requests}).encode()
    response = requests.post(ENDPOINT_URL,
                             data=image_data,
                             params={'key': API_KEY},
                             headers={'Content-Type': 'application/json'})

    if response.status_code != 200 or response.json().get('error'):
        print(response.text)
    else:
        json_response = response.json()['responses']
        response_text = json_response[0]['textAnnotations'][0]['description'].strip()
        response_text_list = response_text.split("\n")
        question = " ".join(response_text_list[:-3])
        options = "\n".join(response_text_list[-3:]).strip("?")
        print question, "\n", options

        # url = "https://en.wikipedia.org/w/index.php?search={}".format(question)
        # webbrowser.open(url)
        words = [word for word in question.split() if word.lower() not in WORDS_TO_STRIP]
        question = ' '.join(words)
        url = "https://www.google.com.tr/search?q={}".format(question)
        webbrowser.open(url)


while(True):
    key_pressed = raw_input('Press ENTER to screenshot live game')
    if key_pressed == '':
        get_question()
