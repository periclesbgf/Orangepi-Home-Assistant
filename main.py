import wave
import numpy as np
from tensorflow.keras import models
from sr.tf_helper import *
import os
from sr.record_audio import record_audio, list_devices, list_output_devices
import openai
from dotenv import load_dotenv
from openai import OpenAI
from google.cloud import speech

from utils.utils import get_local_ip
from utils.constants import commands
from mqtt.mqtt_controller import initialize_mqtt_client

from mqtt.response_handler import handler
import pygame
pygame_menu = pygame
pygame_menu.init()


loaded_model = models.load_model("/home/orangepi/Orangepi-Home-Assistant/model")

load_dotenv()
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
api_key=os.getenv("OPENAI_API_KEY")
client_openai = OpenAI(base_url="https://api.openai.com/v1", api_key=api_key)

def save_predict_delete(data, filename):
    save_audio_data_to_wav(data, filename)
    predict_mic(filename)
    delete_file(filename)

def save_audio_data_to_wav(data, filename):
    try:
        with wave.open(filename, 'wb') as audio_file:
            audio_file.setnchannels(1)  # Mono
            audio_file.setsampwidth(2)   # 16 bits
            audio_file.setframerate(44100)  # Exemplo de taxa de amostragem
            audio_file.writeframes(data)
        return filename
    except Exception as e:
        print(f"Erro ao salvar os dados de áudio como WAV: {e}")

def predict_mic():
    audio = record_audio(device_index=2, duration=1)  # Assegure-se que o índice está correto.

    if audio is None or len(audio) == 0:
        print("Erro: Buffer de áudio está vazio ou não capturado corretamente.")
        return
    spec = preprocess_audiobuffer(audio)
    prediction = loaded_model(spec)
    label_pred = np.argmax(prediction, axis=1)
    command = commands[label_pred[0]]

    if command == 'eden':
        pygame_menu.Color('BLUE')
        pygame_menu.time.get_ticks()
        print("Eden ativado")
        audio = record_audio(device_index=2, duration=4)
        filename = "audio.wav"
        filename = save_audio_data_to_wav(audio, filename)
        text = transc(filename)

        if text == "Não foi possível transcrever o áudio" or text == "":
            print("Erro ao transcrever o áudio")
            return
        handler(text)
        #delete_file(filename)

    print("Predicted:", command)

def delete_file(file):
    try:
        os.remove(file)
    except OSError as e:
        print(f"Erro ao excluir o arquivo {file}: {e}")



def transcrever_audio(arquivo_wav):
    client = speech.SpeechClient.from_service_account_json(google_credentials)

    with open(arquivo_wav, "rb") as audiofile:
        content = audiofile.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="pt-BR"
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

    if response.results:
        return response.results[0].alternatives[0].transcript
    else:
        return ""

def text_to_speech_wav(text, lang='pt-BR'):

    # Solicita a síntese de fala
    response = openai.Audio.create(
        model="tts",
        input=text,
        output="audio/wav"
    )

    audio_file_wav = "speech.wav"

    with open(audio_file_wav, 'wb') as out:
        out.write(response['data'])
        print(f"Arquivo '{audio_file_wav}' salvo com sucesso.")

    return audio_file_wav

def transc(audiofile):
    audio_file = open(audiofile, "rb")
    transcript = client_openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcript

if __name__ == "__main__":

    SERVER_IP = get_local_ip()
    print(f"O IP do servidor foi definido para {SERVER_IP}")

    client = initialize_mqtt_client()
    client.loop_start()
    # Exemplo de uso

    list_devices()

    list_output_devices()
    # client = initialize_mqtt_client()
    # client.loop_start()

    # mqtt_publish("Hello MQTT!")

    while True:
        predict_mic()
#Input Device id  1  -  ahubhdmi: ahub_plat-i2s-hifi i2s-hifi-0 (hw:2,0)
# Input Device id  2  -  USB PnP Sound Device: Audio (hw:3,0)
# Input Device id  6  -  pulse
# Input Device id  10  -  default
# Output Device id  0  -  audiocodec: CDC PCM Codec-0 (hw:0,0)
# Output Device id  1  -  ahubhdmi: ahub_plat-i2s-hifi i2s-hifi-0 (hw:2,0)
# Output Device id  3  -  sysdefault
# Output Device id  4  -  samplerate
# Output Device id  5  -  speexrate
# Output Device id  6  -  pulse
# Output Device id  7  -  upmix
# Output Device id  8  -  vdownmix
# Output Device id  9  -  dmix
