
from xml.etree.ElementTree import *  # Import everything 

import time
from datetime import datetime
import csv
import os

## from xlsxwriter.workbook import Workbook

import numpy as np
import pandas as pd  ## Abbreviate it using the convention
pd.options.display.date_dayfirst=True  # Important to some assumptions below


## Worker Function for checking currency
def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

# It is a good idea to put your variables up front
fewsNamespace="http://www.wldelft.nl/fews/PI"

regionHome = r'C:\Users\Lindsay\Documents\GitHub\DFUDA_2019_Adapter/'

ExportXML = '3_Output/Export_fromGoldSim.xml'

# populate the xml file
def xml(parameter, location, eventValues, dT64, unit):
    #sd = str(dateTime[0])
    sd = dateTime[0].strftime("%Y-%m-%d")
    st = dateTime[0].strftime("%H:%M:%S")
    ed = dateTime[-1].strftime("%Y-%m-%d")
    et = dateTime[-1].strftime("%H:%M:%S")
    DTtimeStep = dateTime[1]-dateTime[0]
    timeStep = int(DTtimeStep.total_seconds())
    
    # write XML output timeseries
    with open(regionHome+ExportXML,'a') as xf:    # 'a+b'
        
        ## Write Header for each Series 
        
        xf.write('    <series>\n')
        xf.write('        <header>\n')
        xf.write('            <type>instantaneous</type>\n')        
        
        loc_text = str('            <locationId>%s</locationId>\n') % (location)
        xf.write(loc_text)        
        
        par_text = str('            <parameterId>%s</parameterId>\n') % (parameter)
        xf.write(par_text)
        
        timestep_text = str('            <timeStep unit="second" multiplier="%s"/>\n') %(timeStep)
        xf.write(timestep_text)   
        
        sd_text = str('            <startDate date="%s" time="%s"/>\n') % (sd, st)
        xf.write(sd_text)
        
        ed_text = str('            <endDate date="%s" time="%s"/>\n') % (ed, et)
        xf.write(ed_text)
        
        xf.write('            <missVal>-999.0</missVal>\n')
        xf.write('            <stationName>Hydro Gauge 1</stationName>\n')        
        
        unit_text = str('            <units>%s</units>\n') %(unit)
        xf.write(unit_text) 
        
        xf.write('        </header>\n')
        
        
        ## Write all the event values for each  timestamp in the series
        for i in range(len(eventValues)):
            event_date = str('        <event date="%s"') % (dateTime[i].strftime("%Y-%m-%d"))
            event_time = str(' time="%s"') % (dateTime[i].strftime("%H:%M:%S"))
            event_value = str(' value="%s"') % eventValues[i][0].round(2)
            event_flag = str(' flag="0"/>\n')
            
            event = str(event_date+event_time+event_value+event_flag)
            xf.write(event)
            
        xf.write('    </series>\n')
        
        

GoldSimOutputs = ['RoutedFlows.txt','RoutedLevels.txt']

DF = pd.DataFrame()

# write XML output header, once
with open(ExportXML,'w') as xf:
    xf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    xf.write('<TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">\n')
    xf.write('    <timeZone>10.0</timeZone>\n')

for GS in GoldSimOutputs:
    fin = os.path.join(regionHome,'2_Model',GS)

    with open(fin,'r') as f:
        lines = f.readlines()
        parameter = lines[11].split()[1]
        unit = lines[12].split()[1]

    df = pd.read_table(fin,skiprows=14,header=None,names=['DateTime',parameter+'_'+unit,'Blank'],index_col=0,
                       parse_dates=True,dayfirst=True)

    df = df.drop(['Blank'],axis=1)   
    DF = pd.concat([DF,df],axis=1)
    
    locn = 'NPD'
    dateTime = df.index.to_pydatetime()
    xml(parameter,locn,df.values,dateTime,unit)

with open(ExportXML,'a') as xf:
    xf.write('</TimeSeries>\n') 

ax=DF.iloc[:,0].plot(legend=True)
DF.iloc[:,1].plot(secondary_y=True,
                  ax=ax,legend=True)
ax.set_ylabel(DF.columns[0])
ax.set_xlim('09-01-2011','13-01-2011')
ax.grid(which='both')

fig = ax.get_figure()
fig.savefig('GoldSim_TS.png',dpi=300)

        