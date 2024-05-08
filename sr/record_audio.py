import pyaudio
import numpy as np

# Configurações
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Instância PyAudio
p = pyaudio.PyAudio()

def list_output_devices():
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxOutputChannels') > 0:
            print("Output Device id ", i, " - ", device_info.get('name'))


def list_devices():
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(0, num_devices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))



def record_audio(device_index, duration=1):
    try:
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            input_device_index=device_index
        )
        frames = []
        for _ in range(int(RATE / FRAMES_PER_BUFFER * duration)):
            data = stream.read(FRAMES_PER_BUFFER)
            frames.append(data)


        stream.stop_stream()
        stream.close()
        return np.frombuffer(b''.join(frames), dtype=np.int16)

    except Exception as e:
        print(f"Erro ao abrir stream: {e}")
        return None

def terminate():
    p.terminate()

