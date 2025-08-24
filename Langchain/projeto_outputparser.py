from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

#A biblioteca pydantic nos permite forçar tipagem no python. Usaremos ela para forçar o formato de saída do outputparser
#Faremos com que um dos dados seja boolean, outro uma lista, etc...
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

#Criamos a classe para conseguirmos o resultado no formato que queremos
class Avaliacao(BaseModel):
    "Review foi enviado por um cliente que comprou um produto, preciso avaliar esse produto para saber se ele é bom e se vale a pena"
    review_positiva: bool = Field(description="Se a review é positiva ou negativa")
    vale_pena: bool = Field(description="Essa avaliação diz que vale a pena ou não comprar esse produto?")
    pontos_positivos: list[str] = Field(description="Lista de pontos positivos do produto caso haja algum")
    pontos_negativos: list[str] = Field(description="Lista de pontos negativos do produto caso haja algum")


#Agora criamos uma classe para receber todas as avaliações de uma vez, ao invés de fazer uma requisição por avaliação.
#Dessa forma, mandamos todas as avaliações em um único pedido e recebemos o resultado também em só uma requisição.
class ListaAvaliacoes(BaseModel):
    avaliacoes: list[Avaliacao] = Field(description="Lista de avaliações de usuários sobre o produto")


#Reviews criados com chat GPT. 
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

#A chain é uma forma de passarmos o resultado de um invoke para outro de forma mais simples.
#Ao invés de fazermos diversos invokes como estávamos fazendo anteriormente, utilizamos agora a chain.
chain = template_final | modelo | parser

#Depois de criada, damos invoke nela, passando os parâmetros do primeiro item da chain:
resposta = chain.invoke({"reviews": reviews})


#Salvando agora nosso resultado no nosso "banco de dados":
with open ("reviews.txt", "w", encoding="utf-8") as arquivo:
    for avaliacao in resposta["avaliacoes"]:
        arquivo.write(f"{avaliacao}\n")


#Vamos agora entrar numa outra fase, usando IA para analisar os dados que extraímos e padronizamos.
#Iremos pegar o resultado da chain anterior e coloca-lo em uma nova chain.

template_analise = PromptTemplate.from_template("""Analise a seguinte lista de reviews de um produto e me diga:
1. Quantas reviews são positivas e quantas são negativas (e o percentual de reviews positivas do total)
2. Qual percentual de reviews diz que vale a pena comprar o produto
3. O ponto positivo que mais aparece e o ponto negativo que mais aparece.
A lista de reviews é essa: {lista_reviews}
""")

template_final_analise = (template_analise + template_idioma)

#Como queremos que a resposta da análise seja um texto simples, utilizamos o StrOutputParser.
parser_texto = StrOutputParser()

chain_analise = template_final_analise | modelo | parser_texto

resposta_analise = chain_analise.invoke({"lista_reviews": resposta})

#Verificação para extrair apenas a parte de resposta do DeepSeek, não o raciocínio que ele fez para obter o resultado
if "</think>" in resposta_analise:
    resposta_analise = resposta_analise.split("</think>")[1]

print(resposta_analise)


'''Note que poderíamos juntar as duas chains em uma só. Deixei separado para facilitar a compreensão e também pois, por enquanto,
é a forma como sei implementar funções 'no meio' da chain. Por exemplo a parte de criar o arquivo de reviews. Se concatenássemos
as duas chains, teríamos que criar uma runnable lambda, que farei em outro arquivo. 
'''