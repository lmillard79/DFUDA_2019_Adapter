from xml.etree.ElementTree import *

import time
from datetime import datetime
from xlsxwriter.workbook import Workbook
import csv
import os
import numpy as np
import pandas as pd

regionHome = r'W:\500_Reference\530_Presentations\04_FEWS User Conference - Australia\2019\Python_LinguaFrancaofFEWS\GoldSim/'

## Define File and Folder Paths
GoldSIMSpreadSheet = '3_Output/FEWS_Import.xlsx'
FEWS_Import = regionHome+'3_Output/FEWS_Import-py.xml'

TXTs = [f for f in os.listdir(regionHome+'/2_Model/') if f.endswith('.txt')]
FEWS_Levels = regionHome+'/2_Model/LakeLevels.xlsx'

DF = pd.read_excel(FEWS_Levels,index_col=1,parse_dates=True,infer_datetime_format=True,dayfirst=True)
DF = DF[['HNPD_OUT']]
DF.columns = ['FEWS_Export']

df = pd.read_table(regionHome+'/2_Model/'+TXTs[1], skiprows=14, 
names=['DateTime','Goldsim','blank'], index_col=0,parse_dates=True,infer_datetime_format=True,dayfirst=True)

df = df[['Goldsim']]
df['Goldsim'] = pd.to_numeric(df['Goldsim'],errors='coerce')

DF1 = pd.concat([DF,df],axis=1)
DF1 = DF1.interpolate()
ax = DF1.plot(figsize=(8,6))
fig = ax.get_figure()
fig.savefig(regionHome+'PLOT.png',dpi=300)


