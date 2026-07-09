# Martianeum - Matura informatyka 2025 maj
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from IPython.display import display

DATA = Path('???')
data = pd.read_csv(DATA / 'martianeum.csv', sep='\t', header=0, encoding='cp1250', index_col=None, decimal=',')
n = data.shape[0]
data['data'] = pd.to_datetime(data['data'], format='%Y-%m-%d')
data['martianeum'] = data['masa [kg]'] * data['zawartosc [%]'] / 100
data.loc[data['zawartosc [%]'] < 1, 'martianeum'] = 0
data['stan'] = [0.0] * n
data['ladunek'] = [False] * n
for i in range(n):
    data.loc[i,'stan'] = data.loc[i,'martianeum'] + (data.loc[i-1,'stan'] if i > 0 else 0)
    if data.loc[i,'stan'] >= 100:
        data.loc[i,'stan'] -= 100
        data.loc[i,'ladunek'] = True
data['okres'] = [i//7 for i in range(n)]
display(data.head())

# podpunkt 1
display(data['masa [kg]'].sum(), data['martianeum'].sum())

# podpunkt 2
zad2 = data.groupby('nazwa_obszaru')['masa [kg]'].mean()
zad2 = zad2.sort_values()
display(zad2.index[0])

# podpunkt 3
masy = data.groupby('okres')['masa [kg]'].sum()
masy = masy.sort_values(ascending=False)
display(masy.head(1))
display(data[data['okres'] == 145].head(1))

# podpunkt 4
zad4 = data.copy()
zad4['rok'] = zad4['data'].dt.year
tabela = zad4.pivot_table(
    index='nazwa_obszaru',
    columns='rok',
    values='data',
    aggfunc='count',
    fill_value=0
)
display(tabela)

tabela.plot(
    kind='bar',
    stacked=True,
    figsize=(12,6)
)
plt.xlabel('Nazwy obszarów')
plt.ylabel('Liczba przewozów ładunku')
plt.title('Liczba przewozów z poszczególnych obszarów Marsa')
plt.legend(title='Rok')
plt.tight_layout()
plt.show()

# podpunkt 5
zad5 = data[data['ladunek'] == True]
display(zad5.shape[0], zad5.iloc[0,0].date(), zad5.iloc[-1,0].date())


