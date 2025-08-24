from langchain_huggingface import HuggingFaceEndpoint 
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

#O langchain permite que você utilize o padrão de mensagens igual ao da openAI, mas também tem uma forma própria de criação: 
load_dotenv()
mensagens = [
    SystemMessage("Responda todas as perguntas de forma curta, mas não tanto. No máximo 150 caracteres."),
    #HumanMessage("Qual é a capital da França?"),
    #AIMessage("A capital da França é Paris.")
]

# Usando o hugging face, precisamos escolher qual llm iremos usar. Chamamos o endpoint e passamos o repoid, que é o nome do modelo.
llm = HuggingFaceEndpoint(repo_id="deepseek-ai/DeepSeek-V3.1")

#Agora sim carregados o modelo:
modelo = ChatHuggingFace(llm=llm)

#prompt = input("Digite sua mensagem para a IA: ")
if __name__ == "__main__":
    prompt = "Qual é a capital da França?"

    mensagens.append(HumanMessage(prompt))


    #As estruturas do langchain que são Runnable precisam do método invoke para serem chamadas. Nele nós passamos os parâmetros que queremos trabalhar
    resposta = modelo.invoke(mensagens)

    print(resposta.content, resposta.type)