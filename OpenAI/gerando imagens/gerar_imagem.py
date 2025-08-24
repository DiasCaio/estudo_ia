from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

cliente = OpenAI()

#Fazemos uma requisição para gerar uma imagem, seguindo o mesmo padrão de: cliente.funcionalidade.ação
resposta_requisicao = cliente.images.generate(
    model="dall-e-3",
    prompt="Neymar jogando futebol em um campo verde, com uma bola de futebol, sob um céu azul",
    size="1024x1024"
)

#O resultado de resposta_requisicao é um objeto que contém os dados da imagem gerada. Precisamos então extrair os dados que queremos

url_imagem = resposta_requisicao.data[0].url  # Obtém a URL da imagem gerada

#Usamos o requests para "baixar" a imagem. Pegamos o conteúdo dela e escrevemos em um arquivo:
informacoes_imagem = requests.get(url_imagem)  # Faz uma requisição para obter a imagem

#print(type(informacoes_imagem))

with open("imagem_gerada.png", "wb") as arquivo_imagem:
    arquivo_imagem.write(informacoes_imagem.content)  # Salva a imagem no arquivo