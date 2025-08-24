from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()


modelo = ChatOpenAI()

parser = StrOutputParser()

template_chat = ChatPromptTemplate(
    [
        SystemMessage("Sempre responda em {idioma}")
    ],
    partial_variables={"idioma": "inglês"}
)

texto_usuario = input("Digite sua mensagem para a IA: ")

mensagem_usuario = HumanMessage(texto_usuario)

template_chat.append(mensagem_usuario) #poderíamos usar o método extend ao invés de append se mensagem_usuario fosse uma lista de mensagens

prompt = template_chat.invoke({"idioma": "inglês"})

resposta = modelo.invoke(prompt)

resposta = parser.invoke(resposta)
print(resposta)

print(template_chat)