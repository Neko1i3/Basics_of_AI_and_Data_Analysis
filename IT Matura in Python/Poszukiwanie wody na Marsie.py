# Poszukiwanie wody na Marsie - Matura informatyka 2025 maj
import pandas as pd
from IPython.display import display
from pathlib import Path
pd.set_option('display.max_colwidth', None)

DATA = Path(r"C:\Users\asnguyen\Documents\Datasets\Zadanie Woda na Marsie\dane")
laz = pd.read_csv(DATA / 'laziki.txt', sep='\t', header=0)
obs = pd.read_csv(DATA / 'obszary.txt', sep='\t', header=0)
pom = pd.read_csv(DATA / 'pomiary.txt', sep='\t', header=0)
pom['data_pomiaru'] = pd.to_datetime(pom['data_pomiaru'])
data = pom.merge(laz, on='nr_lazika').merge(obs, on='kod_obszaru')

# podpunkt 1
zad1 = data[data['glebokosc'] <= 100].groupby('nazwa_obszaru')['ilosc'].sum()
display(zad1.nlargest(1))

# podpunkt 2
zad2 = data.copy()
zad2 = zad2.groupby('nr_lazika').agg(
    nazwa = ('nazwa_lazika','first'),
    pierw = ('data_pomiaru','min'),
    ost = ('data_pomiaru','max')
)
zad2['czas'] = zad2['ost']-zad2['pierw']
display(zad2.nlargest(1,'czas')[['nazwa','pierw','ost']])

# podpunkt 3
zad3 = data.assign(czy = data['rok_wyslania'].eq(data['data_pomiaru'].dt.year))
zad3 = zad3.groupby('kod_obszaru')['czy'].any()
zad3 = zad3[zad3.eq(True)]
display(obs.loc[~obs['kod_obszaru'].isin(zad3.index),'nazwa_obszaru'].sort_values())

# podpunkt 4
zad4 = data[data['wsp_ladowania'].str.contains('S')].assign(
    pN=lambda x: x['wspolrzedne'].str.contains('N'),
    pS=lambda x: x['wspolrzedne'].str.contains('S')
).groupby('nr_lazika').agg(
    nazwa = ('nazwa_lazika','first'),
    czyN = ('pN','any'),
    czyS = ('pS','any')
)
display(zad4.loc[zad4['czyN'] & zad4['czyS'], 'nazwa'])
