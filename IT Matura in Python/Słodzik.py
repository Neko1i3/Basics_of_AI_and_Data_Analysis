# Słodzik - Matura informatyka 2017 maj
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from pathlib import Path
pd.set_option('display.max_colwidth', None)

DATA = Path('???')
cuk = pd.read_csv(DATA / 'cukier.txt', sep='\t', header=0)
cuk['data'] = pd.to_datetime(cuk['data'], yearfirst=True)
cen = pd.read_csv(DATA / 'cennik.txt', sep='\t', header=0, index_col='rok', decimal=',')['cena']

# podpunkt 1
zad1 = cuk.groupby('nip')['waga'].sum()
display(zad1.nlargest(3))

# podpunkt 2
cuk = cuk.assign(
    rok=lambda df: df['data'].dt.year,
    cena=lambda df: df['rok'].map(cen),
    ile=lambda df: df['waga'] * df['cena']
)
display(round(cuk['ile'].sum(),2))

# podpunkt 3
zad3 = cuk.groupby('rok')['waga'].sum()
display(zad3)

plt.figure(figsize=(12, 6))
plt.plot(zad3.index, zad3, marker='o')
plt.yticks([i * 5000 for i in range(9)])
plt.title('Ilość sprzedanego cukru w latach 2005-2014') # tytuł wykresu
plt.xlabel('rok') # opis osi OX
plt.ylabel('Ilość cukru [kg]') # opis osi OY
plt.show()
