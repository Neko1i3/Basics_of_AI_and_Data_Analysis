# Miejscowości w Polsce - Zbiór zadań CKE 2015
import pandas as pd
from pathlib import Path
from IPython.display import display
pd.set_option('display.max_colwidth', None)

DATA = Path('???')
woj = pd.read_csv(DATA / 'wojewodztwa.txt', sep='\t', header=0, encoding='cp1250')
pow = pd.read_csv(DATA / 'powiaty.txt', sep='\t', header=0, encoding='cp1250')
gminy = pd.read_csv(DATA / 'gminy.txt', sep='\t', header=0, encoding='cp1250')
miej = pd.read_csv(DATA / 'miejscowosci.txt', sep='\t', header=0, encoding='cp1250')
data = miej.merge(gminy, on='id_gminy').merge(pow, on='id_powiatu').merge(woj, on='id_wojewodztwa')

# podpuntk 1
# display(miej[miej['typ_miejscowosci'].eq('miasto')].shape[0])
display(miej['typ_miejscowosci'].eq('miasto').sum())

# podpunkt 2
# zad2 = data[data['nazwa_powiatu'].eq('brodnicki')].groupby('typ_miejscowosci')['id_miejscowosci'].count()
zad2 = data.loc[data['nazwa_powiatu'].eq('brodnicki'),'typ_miejscowosci'].value_counts()
display(zad2)

# podpunkt 3
zad3 = pow.merge(woj, on='id_wojewodztwa').assign(ile = lambda df: df.groupby('nazwa_powiatu')['nazwa_powiatu'].transform('size'))
zad3 = zad3[zad3['ile'] > 1].sort_values(['nazwa_powiatu','nazwa_wojewodztwa'])
display(zad3[['nazwa_powiatu','nazwa_wojewodztwa']].drop_duplicates())

# podpunkt 4
zad4 = data[data['nazwa_wojewodztwa'].eq('kujawsko-pomorskie')]
zad4 = zad4.assign(czy = zad4['typ_miejscowosci'].eq('miasto')).groupby('id_gminy')['czy'].any()
display((~zad4).sum())

# podpunkt 5
zad5 = data.assign(czy = data['typ_miejscowosci'].eq('miasto'))
zad5 = zad5.groupby('id_gminy').agg(
    ile = ('id_miejscowosci','nunique'),
    ile_m = ('czy','sum'),
    nazwa_gminy = ('nazwa_gminy','first'),
    nazwa_powiatu = ('nazwa_powiatu','first'),
    nazwa_wojewodztwa = ('nazwa_wojewodztwa','first'),
)
zad5 = zad5[(zad5['ile'] == 1) & (zad5['ile_m'] == 1) & (zad5['nazwa_gminy'].str.startswith('J'))]
display(zad5[['nazwa_gminy','nazwa_powiatu','nazwa_wojewodztwa']].sort_values('nazwa_gminy'))

