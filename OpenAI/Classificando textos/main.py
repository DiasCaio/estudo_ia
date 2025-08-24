from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

cliente = OpenAI()

resposta = cliente.moderations.create(
    model="omni-moderation-latest",
    input="Ver o jogo do fluminense me fez querer arrancar meus olhos fora."
)

moderacao = resposta.results[0]

print(moderacao.flagged)  # Verifica se o conteúdo foi sinalizado
print(moderacao.categories.to_dict())  # Exibe as categorias de moderação