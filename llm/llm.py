from pathlib import Path
import time
import os
from pydub import AudioSegment
from dotenv import load_dotenv
import requests
import json
from openai import OpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
CODE = os.getenv("CODE")
URL = os.getenv("URL")

client = OpenAI(base_url="https://api.openai.com/v1", api_key=api_key)


def post_message(prompt):
    payload = {'question': prompt, 'code': CODE}
    response = requests.post(URL, data=payload)
    response.raise_for_status()
    return response.content

def decode_response(response_content):
    try:
        api_response_str = response_content.decode('utf-8')
        response_list = json.loads(api_response_str)

        print("response_list:", response_list)

        if isinstance(response_list, list) and len(response_list) == 2:
            text = response_list[0]
            return text
        else:
            raise ValueError("Formato inesperado de resposta: {}".format(response_list))
    except Exception as e:
        print(f"Erro ao decodificar a resposta: {e}")
        raise

speech_file_path = Path(__file__).parent / "speech.wav"  # Altera a extensão para .wav

def send_prompt(user_prompt):
    print("Enviando requisição de texto")
    try:
        response_raw = post_message(user_prompt)
        response = decode_response(response_raw)
        print("Response", response)
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None, "Erro na requisição"
    except Exception as e:
        print(f"Erro no processamento da resposta: {e}")
        return None, "Erro no processamento da resposta"

    if response == "Desculpe, não entendi.":
        return None, response
    if response.lower() in ["ligar luminária", "desligar luminária", "ligar luz", "desligar luz", "travar porta", "destravar porta", "checar bomba de água", "ligar válvula", "desligar válvula", "ligar bomba de água", "desligar bomba de água"]:
        return None, response

    response_audio = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=response,
        speed=0.9,
    )

    temp_path = speech_file_path.with_suffix('.mp3')
    with open(temp_path, 'wb') as f:
        f.write(response_audio.content)

    # Converte o arquivo de mp3 para wav
    sound = AudioSegment.from_mp3(temp_path)
    sound.export(speech_file_path, format="wav", parameters=["-ar", str(44100)])

    # Limpa o arquivo mp3 temporário
    os.remove(temp_path)

    return speech_file_path, response
