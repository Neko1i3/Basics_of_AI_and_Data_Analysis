# Oscary - Matura informatyka 2019 maj
import pandas as pd
import numpy as np
from pathlib import Path
from IPython.display import display
pd.set_option('display.max_colwidth', None)

DATA = Path('???')
film = pd.read_csv(DATA / 'filmy.txt', sep='\t', header=0)
akt = pd.read_csv(DATA / 'aktorzy.txt', sep='\t', header=0)
akt['data_ur'] = pd.to_datetime(akt['data_ur'], yearfirst=True)
nag = pd.read_csv(DATA / 'nagrody.txt', sep='\t', header=0)
data = nag.merge(akt, on='id_aktora').merge(film, on='id_filmu')

# podpunkt 1
zad1 = akt['kraj_urodzenia'].value_counts(ascending=True)
display(zad1)

# podpunkt 2
zad2 = data.assign(wiek = data['rok'] - data['data_ur'].dt.year)
display(zad2[['imie','nazwisko','wiek']].nsmallest(1,'wiek'))

# podpunkt 3
goat = data['id_aktora'].mode()[0]
display(data.loc[data['id_aktora'].eq(goat), ['imie','nazwisko','rok','tytul']])

# podpunkt 4
d1 = data[data['kategoria'].str.contains('pierwszoplan')].groupby('id_aktora').agg(
    min1=('rok','min'),
    max1=('rok','max')
)
d2 = data[data['kategoria'].str.contains('drugoplan')].groupby('id_aktora').agg(
    min2=('rok','min'),
    max2=('rok','max')
)
zad4 = akt[['id_aktora','imie','nazwisko']].merge(d1, on='id_aktora').merge(d2, on='id_aktora')
zad4['wynik'] = np.maximum(zad4['max2']-zad4['min1'], zad4['max1']-zad4['min2'])
display(zad4[['imie','nazwisko','wynik']])
