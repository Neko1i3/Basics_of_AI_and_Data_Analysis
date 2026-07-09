# Obserwacje ptaków - Zbiór zadań CKE 2015
import pandas as pd
from pathlib import Path
from IPython.display import display
pd.set_option('display.max_colwidth', None)

DATA = Path('???')
gat = pd.read_csv(DATA / 'gatunki.txt', sep='\t', header=0)
lok = pd.read_csv(DATA / 'lokalizacje.txt', sep='\t', header=0)
obs = pd.read_csv(DATA / 'obserwacje.txt', sep='\t', header=0)
obs['data'] = pd.to_datetime(obs['data'], yearfirst=True)
obs['poczatek'] = pd.to_datetime(obs['poczatek'], yearfirst=True)
obs['koniec'] = pd.to_datetime(obs['koniec'], yearfirst=True)
data = obs.merge(lok, on='ID_lokalizacji').merge(gat, on='ID_gatunku')

# podpunkt 1
zad1 = data['nazwa_zwyczajowa'].value_counts()
display(zad1.head(3))

# podpunkt 2
zad2 = data[data['nazwa_zwyczajowa'].eq('remiz')]
zad2['miesiac'] = zad2['data'].dt.month
zad2 = zad2.groupby('miesiac')['liczebnosc'].sum()
display(zad2[zad2 > 0])

# podpunkt 3
zad3 = data[data['nazwa_lacinska'].str.contains('Corvus') & data['opis'].str.contains('miasto')].groupby('nazwa_zwyczajowa')['lokalizacja'].nunique()
display(zad3)

# podpunkt 4a
zad4a = data.assign(czas = (data['koniec']-data['poczatek']).dt.total_seconds() / 60)
zad4a = zad4a.groupby(['lokalizacja','data','poczatek','koniec'], as_index=False).agg(
    czas = ('czas','first'),
    ile = ('liczebnosc','sum')
)
display(zad4a[['lokalizacja','data','czas','ile']].nlargest(1,'czas'))

# podpunkt 4b
zad4b = zad4a.assign(spr = (zad4a['ile']/zad4a['czas']).round(3))
display(zad4b[['lokalizacja','data','spr']].nlargest(1,'spr'))

# podpunkt 5a
zad5 = data[data['nazwa_zwyczajowa'].eq('zuraw')]
display(zad5['liczebnosc'].sum())

# podpunkt 5b
zad5 = zad5.pivot_table(
    index='zachowanie',
    columns='powiat',
    values='liczebnosc',
    aggfunc='sum',
    fill_value=0
)
display(zad5)
