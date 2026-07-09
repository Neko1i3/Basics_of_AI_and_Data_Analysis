# Instalacje - Matura informatyka 2023 czerwiec
import pandas as pd
from pathlib import Path
from IPython.display import display

DATA = Path('???')
kraje = pd.read_csv(DATA / 'kraje.txt', sep='\t', header=0)
urzadzenia = pd.read_csv(DATA / 'urzadzenia.txt', sep='\t', header=0)
instalacje = pd.read_csv(DATA / 'instalacje.txt', sep='\t', header=0)
instalacje['data_i'] = pd.to_datetime(instalacje['data_i'], dayfirst=True)

# podpunkt 1
zad1 = urzadzenia.merge(instalacje, on='kod_u').groupby('typ_u')['kod_u'].count()
display(zad1)

# podpunkt 2
zad2 = urzadzenia.merge(instalacje, on='kod_u')
zad2 = zad2[(zad2['data_i'].dt.year.eq(2019)) & (zad2['data_i'].dt.month.eq(2))]
zad2 = zad2.groupby('producent_u')['kod_u'].count().sort_values(ascending=False)
display(zad2.head(1))

# podpunkt 3
zad3 = kraje.query("ludnosc_k >= 1000000").merge(instalacje, on='kod_k')
zad3 = zad3.groupby('nazwa_k').agg(
    ile=('kod_u','count'),
    lud=('ludnosc_k','first')
)
zad3['wsp'] = (zad3['ile'] * 1000000 / zad3['lud']).round(2)
display(zad3.sort_values('wsp', ascending=False)['wsp'].head(5))

# podpunkt 4
zad4 = urzadzenia.query("typ_u == 'Tablet'").merge(instalacje, on='kod_u')
zad4 = zad4.groupby(['kod_u','nazwa_u'])['kod_k'].nunique().sort_values(ascending=False)
display(zad4.head(1))
