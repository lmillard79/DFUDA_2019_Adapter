
echo on 
C:

:: Initialise the Executables
set PYEXE="C:\Python27\python.exe"
set EXE=GSPlayer.exe
set RUN=Start /wait %EXE%

:: Housekeeping
::set regionHome="W:\500_Reference\530_Presentations\04_FEWS User Conference - Australia\2019\Python_LinguaFrancaofFEWS\GoldSim"

set regionHome=C:\Users\lmillard\GitRepos\DFUDA_2019_Adapter

:: Pre-Adapter - Grab the FEWS_Export.xml from URBS turn into GoldSim XLSX
%PYEXE% %regionHome%\01_Pre_Adapter.py

:: Runtime - Go Do some GoldSim modelling 
CD "C:\Program Files (x86)\GTG\GoldSim 12.1"
%RUN% -r -x %regionHome%\2_Model\NPD_Routing_v8_simplified.gsp

:: Probably need to do this
CD %regionHome%

:: Post-Adapter - Turn the GoldSim XLSX into a FEWS_Import.xml 
%PYEXE% %regionHome%\03_Post_Adapter.py

%SystemRoot%\System32\rundll32.exe "%ProgramFiles%\Windows Photo Viewer\PhotoViewer.dll", ImageView_Fullscreen %regionHome%\GoldSim_TS.png

pause