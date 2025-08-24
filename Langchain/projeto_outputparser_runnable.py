'''
Esse arquivo é igual ao projeto_outputparser, porém irei usar uma runnable lambda para criar o arquivo de reviews.
Além disso, farei tudo também com uma única chain.
'''

from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda #Adição de importação para criarmos uma RunnableLambda
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Avaliacao(BaseModel):
    "Review foi enviado por um cliente que comprou um produto, preciso avaliar esse produto para saber se ele é bom e se vale a pena"
    review_positiva: bool = Field(description="Se a review é positiva ou negativa")
    vale_pena: bool = Field(description="Essa avaliação diz que vale a pena ou não comprar esse produto?")
    pontos_positivos: list[str] = Field(description="Lista de pontos positivos do produto caso haja algum")
    pontos_negativos: list[str] = Field(description="Lista de pontos negativos do produto caso haja algum")

class ListaAvaliacoes(BaseModel):
    avaliacoes: list[Avaliacao] = Field(description="Lista de avaliações de usuários sobre o produto")


reviews = [
    "Som incrível, os graves são bem definidos e a bateria dura o dia inteiro!",
    "Muito confortável, mas a case poderia ser mais resistente.",
    "A qualidade do som é boa, mas às vezes a conexão cai do nada.",
    "Ótimo custo-benefício, uso todo dia na academia sem problemas.",
    "A bateria não dura tanto quanto o anunciado, fiquei um pouco decepcionado."
]


llm = HuggingFaceEndpoint(repo_id="deepseek-ai/DeepSeek-V3.1")

modelo = ChatHuggingFace(llm = llm)

parser = JsonOutputParser(name="avaliacao_usuario", pydantic_object=ListaAvaliacoes)
instrucoes = parser.get_format_instructions()

template_contexto = PromptTemplate.from_template("Você está avaliando reviews de vários usuários sobre um produto, preciso de algumas informações extraídas de cada review dessa lista de reviews: {reviews}")
template_idioma = PromptTemplate.from_template("Responda em {idioma}", partial_variables={"idioma": "português"})
template_formato = PromptTemplate.from_template("formato da resposta: {formato}", partial_variables={"formato": instrucoes})
template_final = (template_contexto + template_idioma + template_formato)


chain = template_final | modelo | parser


#Estamos pegando o resultado da primeira chain, aplicando o que queremos fazer e depois devolvendo o mesmo resultado
#Pois é o que mandaremos para a entrada da segunda chain.
def salvar_banco(dicionario_avaliacoes):
    with open("reviews.txt", "w", encoding="utf-8") as arquivo:
        for avaliacao in dicionario_avaliacoes["avaliacoes"]: ##### Ponto crítico do comentário "Ponto importante"
            arquivo.write(f"{avaliacao}\n")
    return dicionario_avaliacoes

runnable_salvar = RunnableLambda(salvar_banco)


#Agora que criamos a runnable, criamos as etapas da segunda chain, para conseguirmos separar o código em blocos, facilitando o debug

template_analise = PromptTemplate.from_template("""Analise a seguinte lista de reviews de um produto e me diga:
1. Quantas reviews são positivas e quantas são negativas (e o percentual de reviews positivas do total)
2. Qual percentual de reviews diz que vale a pena comprar o produto
3. O ponto positivo que mais aparece e o ponto negativo que mais aparece.
A lista de reviews é essa: {avaliacoes}
""")

'''Ponto importante: Note que acima estamos utilizando o nome "avaliacoes" para nos referirmos à lista de reviews. 
Isso é importante pois é a chave do dicionário que criamos no fim da primeira chain. Ou seja, precisamos usar o mesmo nome para acessar os dados
corretamente. Note que no outro arquivo, tinhamos uma variável diferente, mas isso era permitido pois enviávamos os dados de forma diferente.
A forma como enviamos os dados para a segunda chain no outro arquivo era através do invoke. Agora, estamos passando os dados diretamente 
na chain.
'''

template_final_analise = (template_analise + template_idioma)

parser_texto = StrOutputParser()

chain_analise = template_final_analise | modelo | parser_texto

#Temos agora a chain inicial, nossa runnable e a chain de analise. Podemos então criar a chain final, juntando todas as etapas.

chain_final = chain | runnable_salvar | chain_analise

resposta_analise = chain_final.invoke({"reviews": reviews})

#Verificação para extrair apenas a parte de resposta do DeepSeek, não o raciocínio que ele fez para obter o resultado
if "</think>" in resposta_analise:
    resposta_analise = resposta_analise.split("</think>")[1]

print(resposta_analise)


'''O passo a passo que fizemos foi: Criar a chain inicial para separarmos os dados no formato que queríamos
Criamos o runnable para salvar os dados em um arquivo (que estamos chamando de "banco de dados")
Criamos a chain de análise para extrair informações relevantes dos reviews.
Concatenamos tudo isso em uma só chain. A etapa final é algo específico dos modelos do deepseek, extraíndo a mensagem gerada e deixando o think
'''