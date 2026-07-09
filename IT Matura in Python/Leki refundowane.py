# Leki refundowane - Zbiór zadań CKE 2015
import pandas as pd
from pathlib import Path
from IPython.display import display
pd.set_option('display.max_colwidth', None)

DATA = Path('???')
recepty = pd.read_csv(DATA / 'recepty.txt', sep='\t', header=0)
recepty['Data'] = pd.to_datetime(recepty['Data'], yearfirst=True)
leki = pd.read_csv(DATA / 'leki_refundowane.txt', sep='\t', header=0, decimal='.')
grupy = pd.read_csv(DATA / 'grupy_lekow.txt', sep='\t', header=0)

# podpunkt 1
zad1 = recepty.groupby('Data')['ID_recepty'].nunique().sort_values(ascending=False)
display(zad1.head(1))

# podpunkt 2
zad2 = leki[leki['Cena_refundowana'] == 0].merge(grupy, on='Id_grupy')
zad2['ile'] = zad2.groupby('Id_grupy')['Kod_leku'].transform('size')
zad2 = zad2.sort_values('ile', ascending=False)
display(zad2['Nazwa_grupy'].head(1))

# podpunkt 3
zad3 = recepty.merge(leki, on='Kod_leku').groupby(recepty['Data'].dt.month).agg(
    ile=('ID_recepty','nunique'),
    suma=('Cena_detaliczna','sum')
)
display(zad3)

# podpunkt 4
zad4 = recepty.merge(leki, on='Kod_leku').merge(grupy, on='Id_grupy')
display(zad4.loc[zad4['Cena_detaliczna'].idxmax(), ['Cena_detaliczna','Nazwa_grupy']])

# podpunkt 5
leki['dopłata'] = leki['Cena_detaliczna'] - leki['Cena_refundowana']
zad5 = recepty.merge(leki, on='Kod_leku')
zad5 = zad5.groupby('ID_recepty').agg(
    data=('Data','first'),
    suma=('dopłata','sum')
)
zad5 = zad5[zad5['suma'] > 2000].sort_values('data')
display(zad5)
