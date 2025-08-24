from datasets import load_dataset

#Temos diversos métodos para baixar uma base de dados no hugging face. A versão que estamos utilizando baixa a base de dados no hd
#Assim não precisamos ocupar a RAM com a base de dados.
ds = load_dataset("facebook/natural_reasoning")

print(ds) #O output é uma lista de dicionários, onde cada dicionário é uma base de dados diferente (train, test, validation).
#No caso desse dataset, temos apenas a base de dados de treino (train).
#Cada base da dados é essencialmente um dicionário, então temos as colunas (features) e as linhas de cada coluna (num_rows).


#Podemos pegar uma linha específica da base de dados:
#print(ds['train'][0]) #Mostra a primeira linha da base de dados de treino.

#Caso eu queira pegar de uma coluna específica, posso fazer:
print(ds['train']['question'][0]) #Mostra a primeira linha da coluna 'question'


'''
Podemos também ao invés de separar o dataset da forma acima, podemos baixar o dataset já separado, como mostraremos a seguir.
Podemos, também, guardar partes do dataset em variáveis, por exemplo:
dataset_treino = ds['train']
Assim podemos utilizar dataset_treino['question'][0] para pegar a primeira linha da coluna 'question' do dataset de treino.
'''

#Baixando o dataset já separado:
#ds_treino = load_dataset("facebook/natural_reasoning", split="train")