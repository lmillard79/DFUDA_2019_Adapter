from xml.etree.ElementTree import *

import time
from datetime import datetime
from xlsxwriter.workbook import Workbook
import csv
import os
import numpy as np
import pandas as pd

fewsNamespace="http://www.wldelft.nl/fews/PI"
parametername='Calculated_Discharge'

regionHome = r'W:\500_Reference\530_Presentations\04_FEWS User Conference - Australia\2019\Python_LinguaFrancaofFEWS\GoldSim/'

## Define File and Folder Paths
FEWS_Export = regionHome+'1_Input/FEWS_Export.xml'
outputCSV = regionHome+'1_Input/FEWS_Input-TEST.csv'
GoldSIMSpreadSheet = 'FEWS_Input-TEST.xlsx'

## Worker Function for checking currency
def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

#######################
with open(FEWS_Export, "r") as file:
    tree = parse(file)

    PItimeSeries = tree.getroot()

    Parameters=PItimeSeries.findall('.//{' + fewsNamespace + '}parameterId')
    ParList=[]
    par =[]
    locId=[]
    for param in Parameters:
        ParList.append(param.text)
        
    missingvalue =PItimeSeries.findall('.//{' + fewsNamespace + '}missVal')

    series = PItimeSeries.findall('.//{' + fewsNamespace + '}series')
    # determine size of aray needed. all series MUST be the same length
    for S in series:
        events = S.findall('.//{' + fewsNamespace + '}event')
        ArrayDates = np.zeros((len(events)),dtype='datetime64[ns]')
        ArrayValues = np.zeros((len(events)))
    j = 0

    DateList = []
    for S in series:
        par = S.find('.//{' + fewsNamespace + '}parameterId').text
        if par!=parametername:
            pass
        
        else:
            i=0
            events = S.findall('.//{' + fewsNamespace + '}event')
            locs = S.findall('.//{' + fewsNamespace + '}locationId')
            
            for l in locs:
                locId.append(l.text)        
        
            for ev in events:
                if ev.attrib['value'] == S.find('.//{' + fewsNamespace + '}missVal').text:
                    ArrayValues[i] = float(0)
                else:
                    ArrayValues[i] = float(ev.attrib['value'])
                
                strucTime_Tuple = datetime.strptime(ev.attrib['date'] + " " + ev.attrib['time'],"%Y-%m-%d %H:%M:%S")
                #date_string = time.strftime('%d/%m/%y %H:%M',strucTime_Tuple)
                ArrayDates[i] = strucTime_Tuple
                #secondsEpoch = time.mktime(strucTime_Tuple)            
                #DateList.append(date_string)
                #Array[i,0] = secondsEpoch

                i = i + 1
            j = j + 1
    row = i
    col = j


DFd = pd.DataFrame(ArrayDates) 
DFv = pd.DataFrame(ArrayValues) 

DF = pd.concat([DFd,DFv],axis=1)
DF.columns = ['DateTime',parametername]
print(DF.head())
#DF = DF[['DateTime','secondsEpoch',parametername]]

#writer = pd.ExcelWriter('1_Input/FEWS_Export-py.xlsx',engine='xlsxwriter',datetime_format='d/mmm/yyyy hh:mm', date_format='dd/mmm/yyyy')

##DF.to_excel(writer, sheet_name='FEWS_Export',index=False)
DF.to_excel('1_Input/FEWS_Export-py.xlsx',sheet_name='FEWS_Export')

