import socket
import wave
import numpy as np
from tensorflow.keras import models
from tf_helper import *
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import speech_recognition as sr
from pydub import AudioSegment
from record_audio import record_audio

from constants import commands

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
#         response_handler(texto_transcrito)
#         return texto_transcrito
#     except sr.UnknownValueError:
#         return "Não foi possível transcrever o áudio"
#     except sr.RequestError as e:
#         return f"Erro na requisição para a API do Google: {e}"

# def response_handler(text):
#     filepath, prompt_output = send_prompt(text)
#     text_lower = prompt_output.lower()
#     if text_lower in ['ligar a luminária', 'ligar luminária','ligue a luminária','ligue luminária', 'ligar luminaria']:
#         command = 'on'
#         mqtt_publish(command, MQTT_TOPIC)
#     elif text_lower in ['desligar a luminária', 'desligar luminária','apagar luminária', 'desligar luminaria', 'desligue a luminária', 'desligue luminária']:
#         command = 'off'
#         mqtt_publish(command, MQTT_TOPIC)
#     elif text_lower in ["tocar musica", "tocar música", "tocar um som", "tocar som"]:
#         pass
#         #send_wav_file_over_tcp(wav_file_path, ESP32_TCP_SERVER_IP, ESP32_TCP_SERVER_PORT_FOR)
#     elif text_lower in ["ligar luz", "ligar a luz", "ligar luz.", "ligue luz.", "ligar a luz"]:
#         command = 'on_light'
#         mqtt_publish(command, "led/debug")
#     elif text_lower in ["desligar luz", "desligar a luz", "desligar luz.", "desligue luz."]:
#         command = 'off_light'
#         mqtt_publish(command, "led/debug")
#     elif text_lower in ["ligar valvula", "ligar a valvula", "ligar valvula.", "ligue valvula."]:
#         command = "1"
#         mqtt_publish(command, "sala11/valvula")
#     elif text_lower in ["desligar valvula", "desligar a valvula", "desligar valvula.", "desligue valvula."]:
#         command = "0"
#         mqtt_publish(command, "sala11/valvula")
#     elif text_lower in ["travar porta", "travar a porta", "travar porta.", "trave porta."]:
#         command = "11111111111111111111"
#         mqtt_publish(command, "esp32/open_door")
#     elif text_lower in ["destravar porta", "destravar a porta", "destravar porta.", "destrave porta."]:
#         command = "00000000000000000000"
#         mqtt_publish(command, "esp32/open_door")
#     elif text_lower in ["ligar bomba de água", "ligar bomba de agua", "ligar bomba de água.", "ligue bomba de água."]:
#         command = "1"
#         mqtt_publish(command, "sala11/bomba")
#     elif text_lower in ["desligar bomba de água", "desligar bomba de agua", "desligar bomba de água.", "desligue bomba de água."]:
#         command = "0"
#         mqtt_publish(command, "sala11/bomba")
#     # else:
#     #     send_wav_file_over_tcp(filepath, ESP32_TCP_SERVER_IP, ESP32_TCP_SERVER_PORT_FOR)


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