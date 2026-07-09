# System kontroli dostępu - Matura informatyka 2022 maj
import pandas as pd
import datetime as dttm
from IPython.display import display
from pathlib import Path
pd.set_option('display.max_colwidth', None)

DATA = Path("???")
kla = pd.read_csv(DATA / 'klasa.txt', sep=';', header=0)
ucz = pd.read_csv(DATA / 'uczen.txt', sep=';', header=0)
ew = pd.read_csv(DATA / 'ewidencja.txt', sep=';', header=0)
ew['Wejscie'] = pd.to_datetime(ew['Wejscie'])
ew['Wyjscie'] = pd.to_datetime(ew['Wyjscie'])
data = ew.merge(ucz, on='IdUcznia').merge(kla, on='IdKlasy')

# podpunkt 1
zad1 = data[data['Imie'].str.endswith('a') & data['ProfilKlasy'].eq('biologiczno-chemiczny')]
display(zad1.shape[0])

# podpunkt 2
data['dzien'] = data['Wejscie'].dt.date
zad2 = data[data['Wejscie'].dt.time <= dttm.time(8, 0, 0)]
zad2 = zad2.groupby('dzien')['IdUcznia'].nunique()
display(zad2)

# podpunkt 3
data['czas'] = (data['Wyjscie'] - data['Wejscie']).dt.total_seconds()
zad3 = data.groupby('IdUcznia').agg(
    imie = ('Imie','first'),
    nazw = ('Nazwisko','first'),
    suma = ('czas','sum')
)
display(zad3.nlargest(3,'suma')[['imie','nazw']])

# podpunkt 4
ob = data.loc[data['dzien'].eq(dttm.date(2022, 4, 6)), 'IdUcznia']
display(ucz[~ucz['IdUcznia'].isin(ob)][['Imie','Nazwisko']])
