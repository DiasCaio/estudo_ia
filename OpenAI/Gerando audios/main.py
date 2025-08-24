from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()

cliente = OpenAI()


#Jeito 1 de gerar áudio, usando um chat por voz:
#na solução abaixo, geramos o áudio usando os métodos de chat. Então geramos o áudio a partir de um prompt.
#Nessa solução, é como se estivéssemos conversando com o ChatGPT, mas ao invés de recebermos uma resposta em texto, recebemos um áudio.
audio1 = cliente.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["audio","text"],
    audio={"format": "wav", "voice": "alloy"}, #Nesse campo podemos escolher o formato, a voz do áudio, a velocidade, etc.
    messages=[{"role":"user", "content":"Crie um áudio sobre Charlie Brown JR"}]
)


#Esse formato é um pouco mais livre, onde podemos escolher o texto do áudio.
audio2 = cliente.audio.speech.create(
    model="tts-1",
    input="Testando o modelo de geração de áudio à partir de texto",
    voice="onyx",
    response_format="wav"
)

#Gerando o arquivo de áudio a partir do primeiro método
faixa_audio = audio1.choices[0].message.audio.data
faixa_audio_bytes = base64.b64decode(faixa_audio)

with open("audio_charlie_brown_jr.wav", "wb") as arquivo_audio:
    arquivo_audio.write(faixa_audio_bytes)  # Salva o áudio gerado



#Gerando o arquivo de áudio a partir do segundo método
audio2.write_to_file("audio_teste.wav")  # Salva o segundo áudio gerado