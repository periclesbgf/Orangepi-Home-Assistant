import numpy as np
from utils.constants import MQTT_TOPIC
from mqtt.mqtt_controller import mqtt_publish
from llm.llm import send_prompt
import pyaudio, wave, os, time

import pygame

DEVICE_INPUT_INDEX = 2
DEVICE_OUTPUT_INDEX = 0
VOLUME = 1.0
LUMINARIA = pygame.USEREVENT + 2
LUZ = pygame.USEREVENT + 3
VALVULA = pygame.USEREVENT + 4
PORTA = pygame.USEREVENT + 5
BOMBA_DE_AGUA = pygame.USEREVENT + 6
MQTT_TOPIC_LUMINARIA = "luminaria/debug"
MQTT_TOPIC_LUZ = "led/debug"
MQTT_TOPIC_VALVULA = "sala11/valvula"
MQTT_TOPIC_PORTA = "esp32/open_door"
MQTT_TOPIC_BOMBA = "sala11/bomba"

def handler(text):
    print(text)
    filepath, prompt_output = send_prompt(text)
    print(prompt_output)
    text_lower = prompt_output.lower()

    if text_lower in ['ligar a luminária', 'ligar luminária', 'ligue a luminária', 'ligue luminária', 'ligar luminaria']:
        command = 'on'
        pygame.event.post(pygame.event.Event(LUMINARIA))
        mqtt_publish(command, MQTT_TOPIC_LUMINARIA)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ['desligar a luminária', 'desligar luminária', 'apagar luminária', 'desligar luminaria', 'desligue a luminária', 'desligue luminária']:
        command = 'off'
        pygame.event.post(pygame.event.Event(LUMINARIA))
        mqtt_publish(command, MQTT_TOPIC_LUMINARIA)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ["ligar luz", "ligar a luz", "ligar luz.", "ligue luz.", "ligar a luz"]:
        command = 'on_light'
        pygame.event.post(pygame.event.Event(LUZ))
        mqtt_publish(command, MQTT_TOPIC_LUZ)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ["desligar luz", "desligar a luz", "desligar luz.", "desligue luz."]:
        command = 'off_light'
        pygame.event.post(pygame.event.Event(LUZ))
        mqtt_publish(command, MQTT_TOPIC_LUZ)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ["ligar válvula", "ligar a válvula", "ligar válvula.", "ligue válvula."]:
        command = "1"
        pygame.event.post(pygame.event.Event(VALVULA))
        mqtt_publish(command, MQTT_TOPIC_VALVULA)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ["desligar válvula", "desligar a válvula", "desligar valvula.", "desligue valvula."]:
        command = "0"
        pygame.event.post(pygame.event.Event(VALVULA))
        mqtt_publish(command, MQTT_TOPIC_VALVULA)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ["travar porta", "travar a porta", "travar porta.", "trave porta."]:
        command = "11111111111111111111"
        pygame.event.post(pygame.event.Event(PORTA))
        mqtt_publish(command, MQTT_TOPIC_PORTA)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ["destravar porta", "destravar a porta", "destravar porta.", "destrave porta."]:
        command = "00000000000000000000"
        pygame.event.post(pygame.event.Event(PORTA))
        mqtt_publish(command, MQTT_TOPIC_PORTA)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ["ligar bomba de água", "ligar bomba de agua", "ligar bomba de água.", "ligue bomba de água."]:
        command = "1"
        pygame.event.post(pygame.event.Event(BOMBA_DE_AGUA))
        mqtt_publish(command, MQTT_TOPIC_BOMBA)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ["desligar bomba de água", "desligar bomba de agua", "desligar bomba de água.", "desligue bomba de água."]:
        command = "0"
        pygame.event.post(pygame.event.Event(BOMBA_DE_AGUA))
        mqtt_publish(command, MQTT_TOPIC_BOMBA)
        play_audio("llm/comando.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    elif text_lower in ["desculpe, não entendi.", "desculpe, não entendi", "não entendi", "não entendi.", "desculpe não entendi."]:
        play_audio("llm/desculpe_melhor_ainda.wav", DEVICE_OUTPUT_INDEX, VOLUME)
    else:
        print("Entrei no ultimo if")
        play_audio(filename=filepath, device_id=DEVICE_OUTPUT_INDEX, volume=VOLUME)

def play_audio(filename: str, device_id: int, volume: float = 1.0):
    filename = str(filename)

    if not os.path.exists(filename):
        print(f"Arquivo não encontrado: {filename}")
        return

    try:
        wf = wave.open(filename, 'rb')
    except IOError as e:
        print(f"Erro ao abrir o arquivo: {e}")
        return

    p = pyaudio.PyAudio()

    try:
        # Verificar o número de canais do dispositivo de saída
        output_device_info = p.get_device_info_by_index(device_id)
        max_output_channels = output_device_info['maxOutputChannels']
        channels = min(wf.getnchannels(), max_output_channels)

        # Configuração da stream de áudio com o dispositivo de saída especificado
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=channels,  # Definir canais conforme a capacidade do dispositivo
                        rate=wf.getframerate(),  # Usa a taxa de amostragem do arquivo
                        output=True,
                        output_device_index=device_id)  # Adicionando o índice do dispositivo de saída

        data = wf.readframes(1024)

        while data:
            # Aumentando o volume dos dados de áudio
            frames = np.frombuffer(data, dtype=np.int16)
            new_frames = (frames * volume).astype(np.int16)
            stream.write(new_frames.tobytes())
            data = wf.readframes(1024)
    except Exception as e:
        print(f"Erro ao tocar o arquivo: {e}")
    finally:
        if 'stream' in locals():
            time.sleep(0.3)
            stream.stop_stream()
            stream.close()
        if 'wf' in locals():
            wf.close()
        p.terminate()