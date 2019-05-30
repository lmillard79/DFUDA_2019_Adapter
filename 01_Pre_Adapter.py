from xml.etree.ElementTree import *  # Import everything 

import time
from datetime import datetime
import csv
import os

import numpy as np
import pandas as pd  ## Abbreviate it using the convention
pd.options.display.date_dayfirst=True  # Important to some assumptions below

# Check what version of the module you are running, lets check Pandas.
pd.__version__

# It is a good idea to put your variables up front
fewsNamespace="http://www.wldelft.nl/fews/PI"
regionHome = r'C:\Users\Lindsay\Documents\GitHub\DFUDA_2019_Adapter/'

XMLs = ['importState','import']

for xml in XMLs:
    fin = os.path.join(regionHome,'1_Input',xml+'.xml')    
    FEWS_Export = fin   #  regionHome+'1_Input/importState.xml'

    parameterNames = ['HNPD_OUT','Reservoir.inflow.forecast', 'Reservoir.outflow.forecast', 'Gate.setting.forecast',]
    spreadsheetNames = {'Reservoir.inflow.forecast':'LakeInflows', 'Reservoir.outflow.forecast':'RegulatorFlows', 'Gate.setting.forecast':'Gates', 'HNPD_OUT':'LakeLevels'}

    for parametername in parameterNames:                   
        ParList=[]
        par =[]
        locId=[]
        i = 0    
        
        with open(FEWS_Export, "r") as file:
            tree = parse(file)
            PItimeSeries = tree.getroot()
            Parameters=PItimeSeries.findall('.//{' + fewsNamespace + '}parameterId')
            for param in Parameters:
                ParList.append(param.text)
                
            missingvalue = PItimeSeries.findall('.//{' + fewsNamespace + '}missVal')
            series = PItimeSeries.findall('.//{' + fewsNamespace + '}series')

            # determine size of aray needed. all series MUST be the same length
            parCount=0
            for S in series:
                events = S.findall('.//{' + fewsNamespace + '}event')
                ArrayDates = np.zeros((len(events)),dtype='datetime64[ns]')
                
                par = S.find('.//{' + fewsNamespace + '}parameterId').text
                if par==parametername:
                    parCount = parCount + 1
            
            ArrayValues = np.zeros((len(events), parCount))
            j = 0

            DateList = []
            for S in series:
                par = S.find('.//{' + fewsNamespace + '}parameterId').text
                
                if par!=parametername:
                    pass
                
                else:            
                    events = S.findall('.//{' + fewsNamespace + '}event')
                    locs = S.findall('.//{' + fewsNamespace + '}locationId')
                    i=0
                    for l in locs:
                        locId.append(l.text)        
                
                    for ev in events:
                        if ev.attrib['value'] == S.find('.//{' + fewsNamespace + '}missVal').text:
                            ArrayValues[i,j] = float(0)
                        else:
                            ArrayValues[i,j] = float(ev.attrib['value'])
                        
                        strucTime_Tuple = datetime.strptime(ev.attrib['date'] + " " + ev.attrib['time'],"%Y-%m-%d %H:%M:%S")
                        ArrayDates[i] = strucTime_Tuple

                        i += 1
                    j +=  1
            row = i
            col = j

            DFd = pd.DataFrame(ArrayDates) 
            DFd.columns = ['DateTime']
            DFv = pd.DataFrame(ArrayValues) 
            DFv.columns = locId

            DF = pd.concat([DFd,DFv],axis=1)
                
            
        if xml == 'importState' and parametername == 'HNPD_OUT':
            GoldSIMSpreadSheet = regionHome+'2_Model/'+spreadsheetNames[parametername]+'.xlsx'
            DF.to_excel(GoldSIMSpreadSheet,sheet_name='FEWS_Export')
        
        elif parametername != 'HNPD_OUT':
            GoldSIMSpreadSheet = regionHome+'2_Model/'+spreadsheetNames[parametername]+'.xlsx'
            DF.to_excel(GoldSIMSpreadSheet,sheet_name='FEWS_Export')
