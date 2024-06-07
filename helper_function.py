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
import pygame
import time
import pyaudio
import threading

from utils.utils import get_local_ip
from utils.constants import commands
from mqtt.mqtt_controller import initialize_mqtt_client

from mqtt.response_handler import handler

EDEN_EVENT = pygame.USEREVENT + 1

loaded_model = models.load_model("model-teste")
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Manter a taxa de amostragem em 44100 Hz
FRAMES_PER_BUFFER = 4096
DEVICE_INPUT_INDEX = 1

load_dotenv()
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
api_key = os.getenv("OPENAI_API_KEY")
client_openai = OpenAI(base_url="https://api.openai.com/v1", api_key=api_key)

def save_predict_delete(data, filename):
    save_audio_data_to_wav(data, filename)
    predict_mic(filename)
    delete_file(filename)

def save_audio_data_to_wav(data, filename):
    try:
        with wave.open(filename, 'wb') as audio_file:
            audio_file.setnchannels(1)  # Mono
            audio_file.setsampwidth(2)  # 16 bits
            audio_file.setframerate(RATE)  # Taxa de amostragem ajustada
            audio_file.writeframes(data)
        return filename
    except Exception as e:
        print(f"Erro ao salvar os dados de áudio como WAV: {e}")

def initialize_stream(p, input_device_index):
    return p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=FRAMES_PER_BUFFER,
                  input_device_index=input_device_index)

def record_audio_thread(audio_buffer, stream):
    try:
        while True:
            data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
            audio_buffer.append(data)
            if len(audio_buffer) * FRAMES_PER_BUFFER >= RATE * 4:  # 4 segundos de áudio
                break
    except IOError as e:
        print(f"Erro na leitura do stream de áudio: {e}")

def predict_mic(pygame_menu):
    p = pyaudio.PyAudio()

    try:
        input_device_index = DEVICE_INPUT_INDEX
        input_device_info = p.get_device_info_by_index(input_device_index)
        if not input_device_info['maxInputChannels'] > 0:
            print(f"Dispositivo de entrada {input_device_index} não está disponível.")
            return
    except IOError as e:
        print(f"Erro ao acessar o dispositivo de entrada: {e}")
        return
    except IndexError as e:
        print(f"Índice do dispositivo de entrada fora do intervalo: {e}")
        return

    stream = None
    try:
        stream = initialize_stream(p, input_device_index)
        audio_buffer = []

        while True:
            try:
                if stream.is_active():
                    audio_buffer = []
                    record_thread = threading.Thread(target=record_audio_thread, args=(audio_buffer, stream))
                    record_thread.start()
                    record_thread.join()

                    if len(audio_buffer) * FRAMES_PER_BUFFER >= RATE * 4:
                        audio_segment = b''.join(audio_buffer[:RATE * 4 // FRAMES_PER_BUFFER])
                        audio_buffer = audio_buffer[RATE * 4 // FRAMES_PER_BUFFER:]

                        spec = preprocess_audiobuffer(np.frombuffer(audio_segment, dtype=np.int16))
                        if spec is None:
                            print("Erro ao preprocessar o segmento de áudio. Continuando com o próximo segmento.")
                            continue

                        try:
                            prediction = loaded_model(spec)
                            label_pred = np.argmax(prediction, axis=1)
                            command = commands[label_pred[0]]

                            if command == 'eden':
                                print("Eden ativado")
                                pygame.event.post(pygame.event.Event(EDEN_EVENT))

                                # Gravar áudio adicional para o comando "Eden"
                                additional_audio = []
                                for _ in range(int(4 * RATE / FRAMES_PER_BUFFER)):  # 4 segundos de áudio
                                    data = stream.read((FRAMES_PER_BUFFER), exception_on_overflow=False)
                                    additional_audio.append(data)

                                audio = b''.join(additional_audio)
                                filename = "audio_segment.wav"
                                save_audio_data_to_wav(audio, filename)
                                print(f"Segmento de áudio salvo em: {filename}")
                                filename = "audio.wav"
                                save_audio_data_to_wav(audio, filename)
                                stream.stop_stream()
                                stream.close()
                                text = transc(filename)
                                stream = initialize_stream(p, input_device_index)

                                if text == "Não foi possível transcrever o áudio" or text == "":
                                    print("Erro ao transcrever o áudio")
                                    continue

                                handler(text, stream)

                        except Exception as e:
                            print(f"Erro ao processar segmento de áudio: {e}")
                    else:
                        time.sleep(0.01)  # Pequeno atraso para evitar sobrecarga
                else:
                    print("Stream inativo, reinicializando stream...")
                    stream.stop_stream()
                    stream.close()
                    stream = initialize_stream(p, input_device_index)
            except IOError as e:
                print(f"Erro na leitura do stream de áudio: {e}")
                if 'stream' in locals():
                    stream.stop_stream()
                    stream.close()
                stream = initialize_stream(p, input_device_index)
                audio_buffer = []  # Limpar o buffer de áudio após erro de overflow

    except Exception as e:
        print(f"Erro na captura de áudio: {e}")
    finally:
        if stream and stream.is_active():
            stream.stop_stream()
            stream.close()
        p.terminate()

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
