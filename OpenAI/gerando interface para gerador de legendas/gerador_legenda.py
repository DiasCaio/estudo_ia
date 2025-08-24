from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment


def legendar(arquivo_video, contexto):
    load_dotenv()

    cliente = OpenAI()
    extensao = arquivo_video.name.split(".")[-1] # Extraindo a extensão do arquivo de vídeo para garantir que o pydub possa ler corretamente

    print(f"Extraindo áudio do vídeo: {arquivo_video} com extensão: {extensao}")

    audio_do_video = AudioSegment.from_file(arquivo_video, format=extensao)
    audio_do_video.export("audio.mp3", format="mp3")  # Exportando o áudio para um arquivo mp3

    with open("audio.mp3", "rb") as audio_file:
        transcricao = cliente.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            language="pt",
            #Se não quisermos gerar o arquivo de legenda, podemos remover a linha abaixo
            response_format="srt", #response format é o formato de saída desejado. Normalmente, a resposta vem como um objeto.
            #utilizando o srt estamos pedindo para que a resposta seja retornada no formato utilizado para legendas.
            prompt=contexto  # prompt é o contexto que você quer que o modelo utilize para gerar a legenda. Ele aproveita também a escrita
            #do prompt para melhorar a precisão da transcrição.
    )
        
    with open("legenda_com_contexto.srt", "w", encoding="utf-8") as legenda_file:
        legenda_file.write(transcricao)
    
    return transcricao
        