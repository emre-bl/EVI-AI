from gtts import gTTS
from playsound import playsound
import os

def text_to_speech(text, lang='tr'):
    tts = gTTS(text=text, lang=lang, slow=False)
    os.makedirs("pipeline_scripts/mobile_app/assets", exist_ok=True)
    tts.save("pipeline_scripts/mobile_app/assets/LLM_output.mp3")
    playsound("pipeline_scripts/mobile_app/assets/LLM_output.mp3")


"""user_input = "sağa dönün"
text_to_speech(user_input, lang='tr')"""