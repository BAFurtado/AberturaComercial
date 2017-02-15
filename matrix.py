import pandas as pd

#rais10 = pd.read_sas('//STORAGE2/FormatoSAS/brasil2010.sas7bdat', format='sas7bdat', encoding='latin-1', chunksize=100)

rais_mg9 = pd.read_sas('//sasworkspace1/publico/Bernardo Alves Furtado (Dirur)/rais/mg09.sas7bdat', format='sas7bdat',
                       encoding='latin-1', chunksize=100)

for chunk in rais_mg9:
    print(chunk)
