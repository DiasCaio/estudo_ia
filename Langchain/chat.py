import streamlit as st
from modelo_huggingface import modelo, mensagens
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


def abrir_chat(prompt, modelo, mensagens):
    if "mensagens" in st.session_state:
        mensagens = st.session_state["mensagens"]
    else:
        st.session_state["mensagens"] = mensagens
    
    if prompt:
        mensagens.append(HumanMessage(prompt))
        resposta = modelo.invoke(mensagens)
        #Como a resposta do modelo já vem como uma classe AI Message, não precisamos separar o conteúdo, como fazíamos no hugging face
        #Podemos simplesmente dar append na resposta inteira.

        #O tratamento abaixo é apenas para o modelo do DeepSeek, ele não precisa ser utilizado normalmente:
        conteudo_resposta = resposta.content
        
        #O Deepseek sempre explica a linha de pensamento dele no conteúdo da resposta. O que estamos fazendo é separando o texto em uma parte
        #antes do pensamento e uma depois do pensamento, pegando apenas o conteúdo original da resposta.
        if "</think>" in conteudo_resposta:
            mensagens.append(AIMessage(conteudo_resposta.split("</think>")[1]))
        #Tratamento comum para qualquer outro modelo:
        else:
            mensagens.append(resposta)

    for mensagem in mensagens:
        if not isinstance(mensagem, SystemMessage):
            with st.chat_message(mensagem.type):
                st.write(mensagem.content)


def aplicativo():
    st.header("Chat com Langchain e OpenAI", divider=True)

    st.markdown("##### Escreva sua mensagem:")

    prompt = st.chat_input("Digite aqui sua mensagem:")

    abrir_chat(prompt, modelo, mensagens)


aplicativo()