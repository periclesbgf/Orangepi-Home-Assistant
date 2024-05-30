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

history = [
    {
        "role": "system", "content": """\
        1. Você é um assistente virtual chamado Éden. Você é capaz de receber perguntas, comandos ou afirmações.\
        2. Seu papel é responder perguntas de maneira amigável.\
        3. Diferencie se um texto vindo do usuário é uma pergunta, comando ou afirmação.\
        4. Você possui uma lista de comandos disponíveis para serem executados.\
        5. Os comandos incluem: "ligar luminária", "desligar luminária", "ligar luz", "desligar luz", "travar porta", "destravar porta",\
            "checar bomba de água", "ligar válvula", "desligar válvula", "ligar bomba de água", "desligar bomba de água".\
        6. Se a entrada do usuário for um comando: Sua tarefa é determinar se a entrada de um usuário é um desses comandos específicos\
            ou algo que se relacione com esses comandos. Se for um comando,\
            retorne exatamente o comando que você entendeu que o usuário quer executar, sem alterar a estrutura e nem adicionar texto a mais.\
        7. Se a entrada do usuário for uma pergunta: Sua tarefa é responder a pergunta de maneira amigável e informativa.\
        8. Se a entrada do usuário for uma afirmação: Sua tarefa é responder a afirmação de maneira amigável e informativa.\
        9. Se a entrada do usuário for algo que não faz sentido: Sua tarefa é responder: 'Desculpe, não entendi.'
        10. Você deve utilizar no máximo 70 palavras para responder a cada pergunta e responde-las toda em Portugues Brasileiro.\
        11. Sua resposta será enviada para o modelo Text-to-Speech da OpenAI para ser convertida em áudio.\
        12. A voz será a "nova". Por favor, gere o texto onde seja parecido com português brasileiro.\
        13. A pergunta do usuário será enviada para você como texto originado do modelo Whisper, então pode ocorrer algumas falhas. Tente entender o que o usuário quer dizer\

        EXEMPLO_1:
            USUÁRIO: "Ligue a luminária."
            ÉDEN: "ligar a luminária"

        EXEMPLO_2:
            USUÁRIO: "Qual é a temperatura atual?"
            ÉDEN: "checar sensor de temperatura"

        EXEMPLO_3:
            USUÁRIO: "Acenda a luz."
            ÉDEN: "ligar luz"

        EXEMPLO_4:
            USUÁRIO: "Quanto é 1 + 1?"
            ÉDEN: "Um mais um é igual a dois."

        EXEMPLO_4:
            USUÁRIO: "Abra a porta."
            ÉDEN: "destravar porta"

        Dado o contexto acima, responda o texto do usuário com base nas instruções fornecidas.\
        """
    },
]

def send_prompt(user_prompt):
    print("Enviando prompt")
    history.append({"role": "user", "content": user_prompt})

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
        temperature=0.5,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}

    print("Esperando resposta")
    model_output = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            model_output += chunk.choices[0].delta.content
    print("Resposta recebida")
    new_message["content"] = model_output
    if new_message["content"] == "Desculpe, não entendi.":
        return None, model_output
    if new_message["content"].lower() in ["ligar luminária", "desligar luminária", "ligar luz", "desligar luz", "travar porta", "destravar porta", "checar bomba de água", "ligar válvula", "desligar válvula", "ligar bomba de água", "desligar bomba de água"]:
        return None, model_output

    history.append(new_message)
    print("Enviando requisicao de audio")
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=new_message["content"]
    )
    print("Resposta de audio recebida")

    # Salva o conteúdo da resposta em um arquivo de áudio temporário no formato mp3
    temp_path = speech_file_path.with_suffix('.mp3')
    with open(temp_path, 'wb') as f:
        f.write(response.content)

    # Converte o arquivo de mp3 para wav
    sound = AudioSegment.from_mp3(temp_path)
    sound.export(speech_file_path, format="wav", parameters=["-ar", str(44100)])
    print("Resposta convertida para áudio")


    # Limpa o arquivo mp3 temporário
    os.remove(temp_path)

    # mixer.music.load(str(speech_file_path))
    # mixer.music.play()

    # Wait for the music to finish playing
    # while mixer.music.get_busy():
    #     time.sleep(1)
    print("retornando audio e texto")

    return speech_file_path, model_output