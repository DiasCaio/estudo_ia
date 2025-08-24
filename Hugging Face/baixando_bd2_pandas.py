import pandas as pd

df = pd.read_csv("hf://datasets/Anthropic/EconomicIndex/release_2025_03_27/automation_vs_augmentation_by_task.csv")

'''Agora estamos baixando a base de dados direto pelo pandas. Devemos usa-la principalmente quando a base de dados é pequena, pois ela
Será carregada na RAM.'''

print(df.head())  # Mostra as primeiras linhas do DataFrame

#A vantagem é que economiza o espaço em disco, pois não precisamos baixar a base de dados no HD, porém pagamos com o uso da RAM.