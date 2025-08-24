from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
#A diferença entre o modelo OpenAI e ChatOpenAI é que o OpenAI é um modelo de text generation, não chat completion. Então não precisamos
#Passar uma lista de mensagens, mas apenas um único prompt.
load_dotenv()
modelo = OpenAI()

#O template de prompt é usado para formatar a entrada para o modelo. Ele facilita a criação do prompt usando variáveis, para que não precisemos
#escrever o prompt manualmente toda vez.
'''
template_prompt = PromptTemplate.from_template("""
Responda ao usuário em no máximo {tamanho} caracteres, responda em {idioma}, independente da língua que o usuário mandar a mensagem.
Pergunta do usuário: {mensagem}
""", partial_variables={
    "tamanho":140,
    "idioma":"português",
    "mensagem":"Qual a melhor fonte para aprender sobre finanças quantitativas e investimentos automáticos? Gostaria de aprender desde questões estatísticas sobre investimentos até como aplicar isso automaticamente. Pode enviar fontes diferentes para temas diferentes."
}) #A partial_variables é um parâmetro onde passamos os valores "default" das variáveis do dicionário. Dessa forma, não precisamos passa-las
#durante a chamada: 
'''
#Uma outra forma de usar o PromptTemplate, diferente da forma comentada acima, é utilizando ele em blocos, como funções
#Para organizarmos melhor o nosso prompt e instruções para a IA, devemos segmentar nosso prompt em partes menores e mais gerenciáveis. Exemplo:

template_forma = PromptTemplate.from_template("Responda de forma educada, porém informal, como se fosse um amigo do usuário")
template_tamanho = PromptTemplate.from_template("Responda ao usuário em no máximo {tamanho} caracteres", partial_variables={
    "tamanho":140
})
template_idioma = PromptTemplate.from_template("Responda em {idioma}", partial_variables={
    "idioma":"inglês"
})
template_mensagem = PromptTemplate.from_template("Pergunta do usuário: {mensagem}")
template_final = (template_forma + template_idioma + template_tamanho + template_mensagem)


prompt = template_final.invoke({
    "tamanho":1000,
    "idioma":"português",
    "mensagem":"Qual a melhor fonte para aprender sobre finanças quantitativas e investimentos automáticos? Gostaria de aprender desde questões estatísticas sobre investimentos até como aplicar isso automaticamente. Pode enviar fontes diferentes para temas diferentes."
})

resposta = modelo.invoke(prompt)

print(resposta)