from pathlib import Path
from openai import OpenAI
import time
import os
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(base_url="https://api.openai.com/v1", api_key=api_key)
speech_file_path = Path(__file__).parent / "speech.wav"  # Altera a extensão para .wav

response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=" ...Comando  Executado.",
    speed=0.9
)
print("Resposta de audio recebida")

temp_path = speech_file_path.with_suffix('.mp3')
with open(temp_path, 'wb') as f:
    f.write(response.content)

# Converte o arquivo de mp3 para wav
sound = AudioSegment.from_mp3(temp_path)
sound.export(speech_file_path, format="wav", parameters=["-ar", str(44100)])
print("Resposta convertida para áudio")

