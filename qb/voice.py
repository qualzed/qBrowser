import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

def voice():
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        
        config_path="config/qb.cfg"
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("language="):
                    lang = line.strip().split("=", 1)[1]
                
        if lang == "ru": speech = r.recognize_google(audio, language="ru-RU")
        elif lang == "en": speech = r.recognize_google(audio, language="en-EN")

        return speech
    except Exception as e:
        print(e)