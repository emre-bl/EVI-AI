from gtts import gTTS
from playsound import playsound
import os

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(script_dir + "/mobile_app/assets", exist_ok=True)
    tts.save(script_dir + "/mobile_app/assets/LLM_output.mp3")
    #playsound("/mobile_app/assets/LLM_output.mp3")


"""user_input = "Checking for obstacles. Be cautious!"
text_to_speech(user_input, lang='en')"""