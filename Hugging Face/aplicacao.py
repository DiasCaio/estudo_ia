import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient



def gerar_texto(prompt):
    st.markdown("##### Peça para o sistema gerar um texto para você:")
    cliente = InferenceClient()
    if prompt:
        mensagens = [
        {"role": "system", "content": "Sua função é dar uma resposta única para uma única frase recebida. Isso não será um chat, mas sim uma resposta direta."},
        {"role": "user", "content": prompt}
        ]

        resposta = cliente.chat_completion(mensagens, model="meta-llama/Llama-3.2-3B-Instruct")
        resposta_ia = resposta.choices[0].message

        content_ia = resposta_ia.content
        st.write(content_ia)

def resumir_texto(prompt):
    st.markdown("##### Escreva o texto que deseja resumir:")
    cliente = InferenceClient()
    if prompt:
        resposta = cliente.summarization(prompt, model="facebook/bart-large-cnn")
        st.write(resposta.summary_text)

def abrir_chat(prompt):
    st.markdown("##### Escreva sua mensagem:")
    cliente = InferenceClient()
    if "mensagens" not in st.session_state:
        mensagens = [
            {"role": "system", "content": "Você é um assistente útil. Responda às perguntas de forma clara, concisa e precisa."}
        ]

        st.session_state["mensagens"] = mensagens
    else:
        mensagens = st.session_state["mensagens"]

    if prompt:
        mensagens.append({"role": "user", "content": prompt})
        resposta = cliente.chat_completion(mensagens, model="meta-llama/Llama-3.2-3B-Instruct")
        resposta_ia = resposta.choices[0].message

        role_ia = resposta_ia.role
        content_ia = resposta_ia.content

        dicionario_ia = {"role": role_ia, "content": content_ia}

        mensagens.append(dicionario_ia)

        for dic_mensagens in mensagens:
            role = dic_mensagens["role"]
            content = dic_mensagens["content"]
            if role != "system":
                with st.chat_message(role):
                    st.write(content)


def main_app():
    st.header("Aplicação de testes", divider=True)

    st.markdown("#### Selecione a opção desejada:")

    opcoes = ["Gerar Texto", "Resumir Texto", "Abrir Chat"]
    ferramenta_selecionada = st.selectbox("Opções:", options=opcoes)

    prompt = st.chat_input("Digite aqui seu prompt:")

    if ferramenta_selecionada:
        if ferramenta_selecionada == opcoes[0]:
            gerar_texto(prompt)
        elif ferramenta_selecionada == opcoes[1]:
            resumir_texto(prompt)
        elif ferramenta_selecionada == opcoes[2]:
            abrir_chat(prompt)

if __name__ == "__main__":
    load_dotenv()
    main_app()