import wave
import numpy as np
from tensorflow.keras import models
from sr.tf_helper import *
import os
from sr.record_audio import record_audio
import whisper
import openai

from utils.utils import get_local_ip
from utils.constants import commands
from mqtt.mqtt_controller import initialize_mqtt_client

from mqtt.response_handler import handler


loaded_model = models.load_model("model")



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
        return filename
    except Exception as e:
        print(f"Erro ao salvar os dados de áudio como WAV: {e}")

def predict_mic():
    audio = record_audio()
    spec = preprocess_audiobuffer(audio)
    prediction = loaded_model(spec)
    label_pred = np.argmax(prediction, axis=1)
    command = commands[label_pred[0]]
    if command == 'eden':
        print("Eden ativado")
        audio = record_audio(duration=3)
        filename = "audio.wav"
        filename = save_audio_data_to_wav(audio, filename)
        text = transcrever_audio(filename)

        if text == "Não foi possível transcrever o áudio" or text == "":
            print("Erro ao transcrever o áudio")
            return
        handler(text)
        delete_file(filename)

    print("Predicted:", command)

def delete_file(file):
    try:
        os.remove(file)
    except OSError as e:
        print(f"Erro ao excluir o arquivo {file}: {e}")

def transcrever_audio(arquivo_wav):
    # Carrega o modelo
    model = whisper.load_model("base")

    # Processa o arquivo de áudio e realiza a transcrição
    result = model.transcribe(arquivo_wav, language="Portuguese")

    # Captura a transcrição do resultado
    texto_transcrito = result["text"]

    # Você pode escolher manipular o texto ou passá-lo diretamente
    return texto_transcrito.strip()

def text_to_speech_wav(text, lang='pt-BR'):

    # Solicita a síntese de fala
    response = openai.Audio.create(
        model="tts",                 # ou outro modelo disponível que você deseja usar
        input=text,
        output="audio/wav"           # Especifica o formato de áudio de saída
    )

    # Nome do arquivo de saída
    audio_file_wav = "speech.wav"

    # Salva o arquivo de áudio
    with open(audio_file_wav, 'wb') as out:
        out.write(response['data'])
        print(f"Arquivo '{audio_file_wav}' salvo com sucesso.")

    # Retorna o caminho do arquivo para possível uso posterior
    return audio_file_wav


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    SERVER_IP = get_local_ip()
    print(f"O IP do servidor foi definido para {SERVER_IP}")

    client = initialize_mqtt_client()
    client.loop_start()

    # mqtt_publish("Hello MQTT!")

    while True:
        predict_mic()
