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
        print("Eden ativado")
        audio = record_audio(device_index=2, duration=3)
        filename = "audio.wav"
        filename = save_audio_data_to_wav(audio, filename)
        text = transcrever_audio(filename)

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
        return "Nenhuma transcrição disponível."

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
