# Stacje benzynowe - Zbiór zadań CKE 2015
import pandas as pd
from pathlib import Path
from IPython.display import display
pd.set_option('display.max_colwidth', None)

DATA = Path('???')
dro = pd.read_csv(DATA / 'drogi.txt', sep='\t', header=0, encoding='cp1250', index_col=None)
kat = pd.read_csv(DATA / 'kategorie.txt', sep='\t', header=0, encoding='cp1250', index_col=None)
siec = pd.read_csv(DATA / 'sieci.txt', sep='\t', header=0, encoding='cp1250', index_col=None)
sta = pd.read_csv(DATA / 'stacje.txt', sep='\t', header=0, encoding='cp1250', index_col=None)
data = sta.merge(siec, on='id_sieci').merge(dro, on='id_drogi').merge(kat, on='id_kategorii')

# podpunkt 1
display(dro['dlugosc'].sum())

# podpunkt 2
zad2 = dro[~dro['id_drogi'].isin(sta['id_drogi'])]
display(zad2[['nazwa','dlugosc']].nlargest(1,'dlugosc'))

# podpunkt 3
zad3 = dro.merge(sta, on='id_drogi').assign(
    ile=lambda x: x.groupby('id_drogi')['id_stacji'].transform('size'),
    sred=lambda x: (x['dlugosc']/x['ile']).round(1)
)
display(zad3[['id_drogi','nazwa','sred']].nsmallest(1,'sred'))

# podpunkt 4
zad4 = dro[dro['nazwa'].str.contains('autostrada', case=False) & ~dro['id_kategorii'].eq('A')]
display(zad4['nazwa'].drop_duplicates())

# podpunkt 5
zad5 = data.pivot_table(
    index='nazwa_sieci',
    columns='kategoria',
    values='id_stacji',
    aggfunc='nunique',
    fill_value=0
)
display(zad5)
