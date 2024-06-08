from pathlib import Path
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
CODE = os.getenv("CODE")
URL = os.getenv("URL")

def post_message(prompt):
    payload = {'question': prompt, 'code': CODE}
    response = requests.post(URL, data=payload)
    response.raise_for_status()
    return response.json()

def save_audio_file(audio_data, file_path):
    with open(file_path, 'wb') as f:
        f.write(audio_data.encode('latin1'))

def send_prompt(user_prompt):
    print("Enviando requisição de texto")
    try:
        response_data = post_message(user_prompt)
        response_text = response_data.get("response")
        audio_data = response_data.get("audio")

        if response_text is None:
            raise ValueError("Campo 'response' não encontrado na resposta")

        if audio_data is not None:
            speech_file_path = Path(__file__).parent / "speech.wav"
            save_audio_file(audio_data, speech_file_path)
            return speech_file_path, response_text
        else:
            return None, response_text
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None, "Erro na requisição"
    except Exception as e:
        print(f"Erro no processamento da resposta: {e}")
        return None, "Erro no processamento da resposta"