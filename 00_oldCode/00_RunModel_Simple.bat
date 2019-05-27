
echo on 
C:

:: Initialise the Executables
set PYEXE="C:\Python27\python.exe"
set EXE=GoldSim.exe
set RUN=Start /wait %EXE%

:: Housekeeping
set regionHome="W:\500_Reference\530_Presentations\04_FEWS User Conference - Australia\2019\Python_LinguaFrancaofFEWS\GoldSim"
DEL %regionHome%\3_Output\Output_ReservoirCalculator02_simple.gsm /Q

:: Pre-Adapter - Grab the FEWS_Export.xml from URBS turn into GoldSim XLSX
PYEXE %regionHome%\1_Input\1_python_XML_to_XLSX.py

:: Runtime - Go Do some GoldSim modelling 
CD "C:\Program Files (x86)\GTG\GoldSim 12.1"
%RUN% -r -save "..\3_Output\Output_ReservoirCalculator02_simple.gsm"  -d "H_Lake_0=25.3m" -x %regionHome%\2_Model\ReservoirCalculator02_simple.gsm

:: Probably need to do this
CD %regionHome%

:: Post-Adapter - Turn the GoldSim XLSX into a FEWS_Import.xml 
PYEXE %regionHome%\3_Output\3c_python_XLSX_to_XML.py"

:: Post-Adapter - Turn the GoldSim XLSX into a FEWS_Import.csv  
::PYEXE %regionHome%\3_Output\3a_python_XLSX_to_CSV.py"


pause