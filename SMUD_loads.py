import pandas as pd
import os

directory = r'S:\ZacharySubins_Documents\SMUD IRP\SMUD Data'
infile = 'Load Forecast Components PST 1312018.csv'
outfile = 'SMUD Load Summary.csv'

df = pd.read_csv(os.path.join(directory, infile), header=0, index_col=[0, 1])

df = df.groupby(['Load Year']).sum() # MWhr

# export
df.to_csv(os.path.join(directory, outfile))