# Perfumeria DlaWas - Matura informatyka 2019 maj
import pandas as pd
from pathlib import Path
from IPython.display import display
pd.set_option('display.max_colwidth', None)

DATA = Path('???')
marki = pd.read_csv(DATA / 'marki.txt', sep='\t', header=0)
perfumy = pd.read_csv(DATA / 'perfumy.txt', sep='\t', header=0)
sklad = pd.read_csv(DATA / 'sklad.txt', sep='\t', header=0)
data = perfumy.merge(sklad, on='id_perfum').merge(marki, on='id_marki')

# podpunkt 1
display(data.loc[data['nazwa_skladnika'].eq('absolut jasminu'), 'nazwa_p'].drop_duplicates())

# podpunkt 2
'''
najtaniej = data.groupby('rodzina_zapachow')['cena'].min()
zad2 = data[data['cena'] == data['rodzina_zapachow'].map(najtaniej)].sort_values('rodzina_zapachow')
'''
idx = perfumy.groupby('rodzina_zapachow')['cena'].idxmin()
display(perfumy.loc[idx, ['rodzina_zapachow', 'nazwa_p', 'cena']].drop_duplicates())

# podpunkt 3
zad3 = data.assign(czy = data['nazwa_skladnika'].str.contains('paczula'))
zad3 = zad3.groupby('nazwa_m')['czy'].any()
display(zad3[~zad3].sort_index())

# podpunkt 4
zad4 = data[(data['nazwa_m'].eq('Mou De Rosine')) & (data['rodzina_zapachow'].eq('orientalno-drzewna'))]
zad4['cena'] = zad4['cena'] * 0.85
display(zad4[['nazwa_p','cena']].sort_values('cena').drop_duplicates())

# podpunkt 5
zad5 = data.copy()
zad5['ile'] = data.groupby('nazwa_m')['rodzina_zapachow'].transform('nunique')
zad5 = zad5[zad5['ile'] == 1]
display(zad5[['nazwa_m','rodzina_zapachow']].drop_duplicates())
