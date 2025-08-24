from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()
cliente = OpenAI()

with open("imagem_gerada.png", "rb") as arquivo_imagem:

    resposta_requisicao = cliente.images.create_variation(
        model="dall-e-2",
        image=arquivo_imagem,  # Caminho para a imagem que você quer modificar
        n=2
    )

print(resposta_requisicao, '\n')

imagens = resposta_requisicao.data

for i, imagem in enumerate(imagens):
    url_imagem = imagem.url  # Obtém a URL da imagem modificada
    informacoes_imagem = requests.get(url_imagem)  # Faz uma requisição para obter a imagem
    with open(f"imagem_modificada_{i}.png", "wb") as arquivo_saida:
        arquivo_saida.write(informacoes_imagem.content)  # Salva a imagem modificada