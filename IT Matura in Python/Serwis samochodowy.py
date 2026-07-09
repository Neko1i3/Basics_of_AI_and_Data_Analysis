# Serwis samochodowy - Matura informatyka 2024 grudzień
import pandas as pd
from pathlib import Path
from IPython.display import display
pd.set_option('display.max_colwidth', None)

DATA = Path('???')
sam = pd.read_csv(DATA / 'samochody.txt', sep='\t', header=0)
usl = pd.read_csv(DATA / 'uslugi.txt', sep='\t', header=0)
wyk = pd.read_csv(DATA / 'wykonane.txt', sep='\t', header=0)
wyk['data'] = pd.to_datetime(wyk['data'], yearfirst=True)
data = wyk.merge(usl, on='id_uslugi').merge(sam, on='nr_rejestracyjny')

# podpunkt 1
display(data.loc[~data['nr_rejestracyjny'].str.startswith('S'),'nr_rejestracyjny'].nunique())

# podpunkt 2
x = data['usluga'].mode()[0]
display(data[data['usluga'].eq(x)].shape[0])
'''
zad2 = data.assign(czy = data['usluga'].eq(x))
zad2 = zad2.groupby('marka')['czy'].sum()
display(zad2[zad2 == 0]) # dobrze
'''
marki = data.groupby('marka')['usluga'].apply(lambda s: (s == x).any())
display(marki[~marki])

# podpunkt 3
zad3 = data.groupby('id_wlasciciela')['cena'].sum()
x = zad3.idxmax()
display(x)
display(data.loc[data['id_wlasciciela'].eq(x),['nr_rejestracyjny','usluga']].drop_duplicates()) # nice

# podpunkt 4
zad4 = data.groupby(data['data'].dt.month)['cena'].sum()
display(zad4.loc[11], zad4.loc[12]) # dobrze
