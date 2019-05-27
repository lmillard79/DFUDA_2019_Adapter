import datetime as dt
import getopt, sys, os
from xml.etree.ElementTree import *
from datetime import *
from time import mktime
import time as TIME
import csv
import pandas as pd
import numpy as np


# input and output file names

# module to round time stamps
def roundTime(DT=None, roundTo=1):
   if DT == None : DT = dt.datetime.now()
   seconds = (DT - DT.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return DT + dt.timedelta(0,rounding-seconds,-DT.microsecond)

# populate the xml file
def xml(parameter, location, value, time, unit, timestep):
    sd = str(dt.datetime.date(time[0]))
    st = str(dt.datetime.time(time[0]))
    ed = str(dt.datetime.date(time[-1]))
    et = str(dt.datetime.time(time[-1]))

    with open(TUFLOW_OUT_XML,'a+b') as xf:
        xf.write('    <series>\n')
        xf.write('        <header>\n')
        xf.write('            <type>instantaneous</type>\n')        
        loc_text = str('            <locationId>%s</locationId>\n') % (location)
        xf.write(loc_text)        
        par_text = str('            <parameterId>%s</parameterId>\n') % (parameter)
        xf.write(par_text)
        timestep_text = str('            <timeStep unit="second" multiplier="%s"/>\n') %(int(timestep))
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
        for i in range(len(value)):
            event_date = str('        <event date="%s"') % (str(dt.datetime.date(time[i])))
            event_time = str(' time="%s"') % (str(dt.datetime.time(time[i])))
            event_valu = str(' value="%s"') % value[i]
            event_flag = str(' flag="0"/>\n')
            event = str(event_date+event_time+event_valu+event_flag)
            xf.write(event)
        xf.write('    </series>\n')
    

def xmlend(parameter, location, value, time, unit,timestep):
    sd = str(dt.datetime.date(time[0]))
    st = str(dt.datetime.time(time[0]))
    ed = str(dt.datetime.date(time[-1]))
    et = str(dt.datetime.time(time[-1]))
        
    with open(TUFLOW_OUT_XML,'a+b') as xf:
        xf.write('    <series>\n')
        xf.write('        <header>\n')
        xf.write('            <type>instantaneous</type>\n')        
        loc_text = str('            <locationId>%s</locationId>\n') % (location)
        xf.write(loc_text)        
        par_text = str('            <parameterId>%s</parameterId>\n') % (parameter)
        xf.write(par_text)
        timestep_text = str('            <timeStep unit="second" multiplier="%s"/>\n') %(int(timestep))
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
        for i in range(len(value)):
            event_date = str('        <event date="%s"') % (str(dt.datetime.date(time[i])))
            event_time = str(' time="%s"') % (str(dt.datetime.time(time[i])))
            event_valu = str(' value="%s"') % value[i]
            event_flag = str(' flag="0"/>\n')
            event = str(event_date+event_time+event_valu+event_flag)
            xf.write(event)
        xf.write('    </series>\n')        
        
        ## Only difference with xml()
        xf.write('</TimeSeries>')        
           
        
def main(TUFLOW_OUT_XML,TUFLOW_PO):
    
    ### ---- Get Model Run Data from INPUT XML ----     
    inputXML = r"D:\FEWS\FEWS_Standalone\FEWS_2017_01_EstryFastModel\Modules\ESTRY\lowerBrisbane\Input\inputLower.xml"  
    #start = a
    #begin = []
    startTime = []
    
    with open(inputXML, "r") as xmlin:
        lines = xmlin.readlines()
        
    #try:
        for l in lines: 
            if 'timeStep' in l:
                ts = l 
                timestep = ts.split()[2].split('=')[-1][1:-3]        
            if 'startDate' in l:
                start = l
                stD = start.split()[1][6:-1]
                stT = start.split()[2][6:-3]
                startTime = TIME.strptime(stD+" "+stT,"%Y-%m-%d %H:%M:%S")
                begin = TIME.mktime(startTime)                
            if 'endDate' in l:        
                end = l
                endD = end.split()[1][6:-1]
                endT = end.split()[2][6:-3]
                endTime = TIME.strptime(endD+" "+endT,"%Y-%m-%d %H:%M:%S")
                ending = TIME.mktime(endTime)
                
                timediff = (TIME.mktime(endTime) - TIME.mktime(startTime))/60/60
                
                with open('end_time.trd', 'w') as f:    
                    f.write('! simulation start time:'+str(datetime.fromtimestamp(begin))+' to ')
                    f.write(str(datetime.fromtimestamp(ending))+'\n')
                    f.write('End Time == %f' %(timediff))
                
                break
            



    
    ###________________________________________________________
    
    #lowerBris_FAST-0403_FEWS_FAST_1d_Q.csv
    #simID = TUFLOW_PO[-34:-10]
    
    simID1 = TUFLOW_PO.split('\\')[-1]
    simID2 = simID1.split('_')[:-2]  # throw away the 1d_Q.csv
    param1 = simID1.split('_')[-2:]
    simID = '_'.join(str(x) for x in simID2)    
    param = '_'.join(str(x) for x in param1)    
   
    
    # write XML output header
    with open(TUFLOW_OUT_XML,'w') as xf:
        xf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xf.write('<TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">\n')
        xf.write('    <timeZone>10.0</timeZone>\n')

    # predefine some variables
    data=pd.DataFrame()
    time=[]
    date=[]

    # open the TUFLOW _PO.csv file           
    with open(TUFLOW_PO, 'rb') as f:  #csvfile
        reader = csv.reader(f, delimiter=',', quotechar='"')
        header = reader.next()  #next line of csv 
     
    header[0]='Timestep'
    header[1]='Time'
    i=1           
    
    for col in header[2:]:    # each item after Time and Timestep column headers
        i= i+1
        if param == '1d_Q.csv':
            prefix = 'Q'
            parameter = 'Flow'
            unit = 'm3//s'
        elif param == '1d_H.csv':
            prefix = 'H'
            parameter = 'Water Level'
            unit = 'm'
        else:        
            prefix = 'Q'
            parameter = 'check'
            unit = 'blah'    
        
        a = col[len(prefix)+1:]   # strip the Prefix i.e. H 
        indA = a.find(simID)
        indB = a.rfind('[') #find last occurrence of [
        if (indA >= 0) and (indB >= 0): # strip simulation ID from header
            a = a[0:indB-1]  # returns just the location name                
        header [i] = a     
        
    try:        
        data = pd.read_csv(TUFLOW_PO, header=0, names=header)
 
    except:
        print 'here'
        message = 'ERROR - Error reading data from: '+TUFLOW_PO
        error = True
        return error, message   
      
    # extract simulation start/end time
    '''
    with open(tufl_trd,('r')) as rf:
        for line in rf:            
            if 'simulation start time =' in line:
                d=str(line[26:36])
                t=str(line[37:45])
                yy, mm, dd = [int(a) for a in d.split('-')]
                hh, mn, ss = [int(a) for a in t.split(':')]
                timeorig=dt.datetime(yy,mm,dd,hh,mn,ss)
            if 'End Time' in line:
                com, dur = [a.strip() for a in line.split('==')]
                timeend =timeorig+dt.timedelta(hours=float(dur))
    '''
    timeorig = dt.datetime(*startTime[:6])
    timeend = timeorig+dt.timedelta(hours=float(timediff))
    # put time series results in an output XML file

    for i in range(data.shape[1]-1):                # i  Number of columns/locations 
        value = []                                  # reset the value variable list
        for j in range(data.shape[0]-1):            # j is Number of rows / time records           
            if i is 0:              # first column is blank
                next
            elif i is 1:            # time column                
                t = timeorig+dt.timedelta(hours=float(data.iloc[j,i]))  #--- 
                t = roundTime(t,roundTo=1)        
                time.append(t)
            else:
                value.append(data.iloc[j,i])         
        locn = data.iloc[:,i].name
        locn = locn.split('[')[0].strip()

        if i > 1:                   # for each data column, generate output XML entry            
            xml(parameter, locn, value, time, unit,timestep)
            
        #END IF
        if i == data.shape[1]-2:      # close out XML file             
            xmlend(parameter, locn, value, time, unit,timestep)          		          
       		          
          
if __name__ == '__main__':
    '''
    Add Arguments into python script

A = The tuflow output XML which will be read into FEWS
B = The TUFLOW PO csv file
C = TUFLOW read file

set A=%ROOT_DIR%\output\outputH.xml   outputQ.xml 
set B=%ROOT_DIR%\Output\plot\csv\lowerBris_FAST-0403_FEWS_FAST_1d_H.csv  lowerBris_FAST-0403_FEWS_FAST_1d_Q.csv
set C=%ROOT_DIR%\end_time.trd
        '''
    try:
        #opts, args = getopt.getopt(sys.argv[1:], "A:B:C:")
        opts, args = getopt.getopt(sys.argv[1:], "A:B:")
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err)
        sys.exit('ERROR: Unknown Argument')

    for o, a in opts:
        if o == "-A":
            TUFLOW_OUT_XML = a
        elif o in ("-B"):
            TUFLOW_PO = a
        #elif o in ("-C"):
        #    tufl_trd = a
        else:
            assert False, "unhandled option"

    nArg = len((sys.argv[1:]))
    if nArg > 4:
        print('ERROR:\nPost adapter is expecting Three arguments. Please check.')
        print('The following arguments are expected:\n-A = The tuflow output XML which will be read into FEWS,\n-B = The TUFLOW PO csv file\n-C = TUFLOW read file')
        sys.exit('ERROR: The following arguments are expected:\n-A = The tuflow output XML which will be read into FEWS,\n-B = The TUFLOW PO csv file\n-C = TUFLOW read file')
    elif nArg < 4:
        print('ERROR:\nPost adapter is expecting Three arguments. Please check.')
        print('The following arguments are expected:\n-A = The tuflow output XML which will be read into FEWS,\n-B = The TUFLOW PO csv file\n-C = TUFLOW read file')
        sys.exit('ERROR: The following arguments are expected:\n-A = The tuflow output XML which will be read into FEWS,\n-B = The TUFLOW PO csv file\n-C = TUFLOW read file')


    # Call the function doing all the work
    main(TUFLOW_OUT_XML,TUFLOW_PO)
