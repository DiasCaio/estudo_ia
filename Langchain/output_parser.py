'''Nesse arquivo estudaremos sobre Output Parsers. Eles servem para processarmos a forma de saída de uma IA.
Por exemplo, supondo que peçamos uma lista de itens para a IA. A resposta dela será um texto formatado como uma lista,
mas na verdade será apenas um texto corrido. Precisamos de um Output Parser para transformar esse texto em uma lista do python, por exemplo.
'''

from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.output_parsers import CommaSeparatedListOutputParser #Temos diversos tipos de output parsers. Escolher o que combina com a situação
from dotenv import load_dotenv

load_dotenv()

modelo = OpenAI()
parser = CommaSeparatedListOutputParser()


template_formato = PromptTemplate.from_template("Formato da resposta: {formato}", partial_variables={
    "formato": parser.get_format_instructions()
})

template_forma = PromptTemplate.from_template("Responda apenas uma lista com as informações pedidas, sem nenhum texto a mais")

template_idioma = PromptTemplate.from_template("Responda em {idioma}", partial_variables={
    "idioma":"português"
})

template_mensagem = PromptTemplate.from_template("Pergunta do usuário: {mensagem}")

template_instruções = PromptTemplate.from_template("Você pode responder com itens em outras línguas, não se prenda à nacionalidade/língua do usuário.")

template_final = (template_forma + template_idioma + template_mensagem + template_instruções)

prompt = template_final.invoke({
#    "mensagem": "Quais os 10 melhores livros sobre finanças quantitativas? Com finanças quantitativas, me refiro à investimentos com base em dados e análises estatísticas."
    "mensagem": "Gere uma base com 5 clientes fictícios"
    #o exemplo acima é utilizando uma IA para gerar base de dados fictícia
})

resposta = modelo.invoke(prompt)

resposta = parser.invoke(resposta)
print(resposta)

'''O método get_format_instructions nos diz o formato ideal para o parser trabalhar. Podemos usa-lo como prompt template para obtermos 
melhores resultados. Observe a linha template_forma:
'''

#print(parser.get_format_instructions())

print(type(resposta))