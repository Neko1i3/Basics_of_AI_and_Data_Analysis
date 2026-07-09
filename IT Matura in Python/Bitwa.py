# Bitwa - Matura informatyka 2021 maj
import pandas as pd
from pathlib import Path
from IPython.display import display

DATA = Path('???')
gracze = pd.read_csv(DATA / 'gracze.txt', sep='\t', header=0, encoding='cp1250')
gracze['data_dolaczenia'] = pd.to_datetime(gracze['data_dolaczenia'], yearfirst=True)
klasy = pd.read_csv(DATA / 'klasy.txt', sep='\t', header=0, encoding='cp1250')
jednostki = pd.read_csv(DATA / 'jednostki.txt', sep='\t', header=0, encoding='cp1250')

# podpunkt 1
r2018 = gracze[gracze['data_dolaczenia'].dt.year == 2018]
zad1 = (r2018.groupby('kraj')['id_gracza'].nunique())
display(zad1.nlargest(5))

# podpunkt 2
elfy = jednostki[jednostki['nazwa'].str.contains('elf') == True]
merged_elfy = elfy.merge(
    klasy,
    on='nazwa',
    validate='many_to_one'
)
zad2 = merged_elfy.groupby('nazwa', as_index=False)['strzal'].sum()
display(zad2)

# podpunkt 3
arty = gracze.merge(
    jednostki,
    on='id_gracza',
    how='left',
    validate='one_to_many'
)
# alternatywa: arty.groupby('id_gracza')['nazwa'].apply(lambda x: (x == 'artylerzysta').any())
arty['czy'] = (arty['nazwa'] == 'artylerzysta')
zad3 = arty.groupby('id_gracza', as_index=False)[['czy']].sum()
indeksy = zad3[zad3['czy'] == 0]['id_gracza']
for id in indeksy.sort_values().values:
    display(id)

# podpunkt 4
jednostki = jednostki.merge(
    klasy,
    on='nazwa',
    validate='many_to_one'
)
brama = jednostki[abs(jednostki['lok_x']-100) + abs(jednostki['lok_y']-100) <= jednostki['szybkosc']]
zad4 = brama.groupby('nazwa', as_index=False)['id_jednostki'].nunique()
display(zad4)

# podpunkt 5
jednostki = jednostki.merge(
    gracze,
    on='id_gracza',
    validate='many_to_one'
)
bitwy = jednostki[['id_jednostki','lok_x','lok_y','id_gracza','kraj']]
# bitwy['czy'] = bitwy['kraj'].eq('Polska')
bitwy = bitwy.groupby(['lok_x','lok_y'], as_index=False).agg(
    ile=('id_gracza','nunique'),
    polska=('kraj', lambda x: (x == 'Polska').any())
)
bitwy = bitwy[bitwy['ile'] > 1]
display(bitwy.shape[0])
display(bitwy[bitwy['polska']].shape[0])


