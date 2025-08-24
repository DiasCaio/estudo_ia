from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
cliente = InferenceClient(model="meta-llama/Llama-3.2-3B-Instruct")

mensagens = [
    {"role": "system", "content": "Você é um assistente útil. Responda às perguntas de forma clara, concisa e precisa."}
]

while True:

    prompt_usuario = input("Digite sua mensagem (ou 'sair' para encerrar): ")

    if prompt_usuario.lower() == "sair":
        break

    mensagens.append({"role": "user", "content": prompt_usuario})

    resposta = cliente.chat_completion(mensagens)


#A resposta da IA como um todo está dentro de choices[0].message. Lá teremos os parâmetros tanto de role quanto de content.

    resposta_ia = resposta.choices[0].message

    role_ia = resposta_ia.role
    content_ia = resposta_ia.content

    dicionario_resposta_ia = {
        "role": role_ia,
        "content": content_ia
    }
    mensagens.append(dicionario_resposta_ia)
    
    print(content_ia)