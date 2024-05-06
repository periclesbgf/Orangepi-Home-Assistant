import socket
import wave
import numpy as np
from tensorflow.keras import models
from sr.tf_helper import *
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import speech_recognition as sr
from pydub import AudioSegment
from sr.record_audio import record_audio
from gtts import gTTS

from utils.constants import commands, MQTT_TOPIC
from mqtt.mqtt_controller import mqtt_publish, initialize_mqtt_client

#from mqtt.response_handler import handler

#from llm import send_prompt

loaded_model = models.load_model("model")

def get_local_ip():
    try:
        # Cria um socket DGRAM
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        print(f"Erro ao obter o endereço IP local: {e}")
        ip = "127.0.0.1"
    return ip

def save_predict_delete(data, filename):
    save_audio_data_to_wav(data, filename)
    predict_mic(filename)
    delete_file(filename)

def save_audio_data_to_wav(data, filename):
    try:
        with wave.open(filename, 'wb') as audio_file:
            audio_file.setnchannels(1)  # Mono
            audio_file.setsampwidth(2)   # 16 bits
            audio_file.setframerate(16000)  # Exemplo de taxa de amostragem
            audio_file.writeframes(data)
    except Exception as e:
        print(f"Erro ao salvar os dados de áudio como WAV: {e}")

# def predict_mic(file):
#     audio = record_audio_from_file(file)
#     spec = preprocess_audiobuffer(audio)
#     prediction = loaded_model(spec)
#     label_pred = np.argmax(prediction, axis=1)
#     command = commands[label_pred[0]]
#     if command == 'eden':
#         activation_word = b'eden'
#         connect_to_esp32_tcp_server(activation_word)
#     print("Predicted:", command)

def predict_mic():
    audio = record_audio()
    spec = preprocess_audiobuffer(audio)
    prediction = loaded_model(spec)
    label_pred = np.argmax(prediction, axis=1)
    command = commands[label_pred[0]]
    print("Predicted:", command)

def delete_file(file):
    try:
        os.remove(file)
    except OSError as e:
        print(f"Erro ao excluir o arquivo {file}: {e}")


# def transcrever_audio(arquivo_wav):
#     recognizer = sr.Recognizer()

#     with sr.AudioFile(arquivo_wav) as source:
#         audio = recognizer.record(source)

#     try:
#         texto_transcrito = recognizer.recognize_google(audio, language='pt-br')
#         handler(texto_transcrito)
#         return texto_transcrito
#     except sr.UnknownValueError:
#         return "Não foi possível transcrever o áudio"
#     except sr.RequestError as e:
#         return f"Erro na requisição para a API do Google: {e}"



def text_to_speech_wav(text, lang='pt-br'):
    # Cria um objeto gTTS
    tts = gTTS(text=text, lang=lang, slow=False)

    # Gera um arquivo temporário mp3
    temp_mp3 = "temp.mp3"
    tts.save(temp_mp3)

    # Converte o arquivo mp3 para wav
    audio = AudioSegment.from_mp3(temp_mp3)
    audio_file_wav = "speech.wav"
    audio.export(audio_file_wav, format="wav")

    # Remove o arquivo temporário mp3
    os.remove(temp_mp3)

    print(f"Arquivo '{audio_file_wav}' salvo com sucesso.")


if __name__ == "__main__":
    SERVER_IP = get_local_ip()
    print(f"O IP do servidor foi definido para {SERVER_IP}")

    # client = initialize_mqtt_client()
    # client.loop_start()

    # mqtt_publish("Hello MQTT!")

    while True:
        predict_mic()