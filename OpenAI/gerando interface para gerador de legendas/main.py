from gerador_legenda import legendar
import streamlit as st


def aplicativo():
    st.header("Gerador de Legendas")
    st.markdown("#### Gere a legenda do seu vídeo (ou áudio) com facilidade usando a API da OpenAI")

    contexto = st.text_input("Escreva o contexto para a legenda (opcional):")
    arquivo = st.file_uploader("Carregue seu vídeo ou áudio", type=["mp4", "mp3", "wav"])

    if arquivo:
        legenda = legendar(arquivo, contexto)
        st.write(f"Arquivo {arquivo.name} gerada com sucesso!")
        st.write(f"Legenda gerada: {legenda}")

if __name__ == "__main__":
    aplicativo()