from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI()

contexto = "Escreva Full Stack separado e completaço com ç"

with open("audio.mp3", "rb") as audio_file:
    transcricao = cliente.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        language="pt",
        #Se não quisermos gerar o arquivo de legenda, podemos remover a linha abaixo
        response_format="srt", #response format é o formato de saída desejado. Normalmente, a resposta vem como um objeto
        #utilizando o srt estamos pedindo para que a resposta seja retornada no formato utilizado para legendas.
        prompt=contexto  # prompt é o contexto que você quer que o modelo utilize para gerar a legenda. Ele aproveita também a escrita
        #do prompt para melhorar a precisão da transcrição.
)

print(transcricao)


with open("legenda_com_contexto.srt", "w", encoding="utf-8") as legenda_file:
    legenda_file.write(transcricao)
    