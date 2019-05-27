# Delft FEWS User Day - May 2019
**Lindsay Millard, Seqwater** 

[![View Lindsay Millard's profile on LinkedIn](https://www.linkedin.com/img/webpromo/btn_viewmy_160x33.png)](https://www.linkedin.com/in/lindsaymillard/)


To demonstrate how to implement an adapter in Delft-FEWS I have put together a Jupyter Notebook, 
see: *Worked_Example_FEWS-GoldSim-Adapter.ipynb*
This Notebook includes comments and can be run step-by-step to understand what is happening. The notebook can be run in the Azure notebooks instance. Due to For loops it won't run seamlessly, it will need the GoldSim Player installed and will need to be controlled by a master file. 

A batch file can be used to control the workflow and python files. To demonstrate the complete workflow the files in this project folder can be downloaded. Example FEWS XML timeseries are also provided to commence the workflow. 
The local computer will need [Goldsim Player 12.1](https://www.goldsim.com/web/customers/downloads/player/)

0. `00_RunPlayerSimple.bat` Will trigger the workflow and call the following files:
1.   `01_Pre_Adapter.py` will convert the XMLs in the \01_Input\ folder into (.xlsx) files for GoldSim
2.   The batch file will then run the Goldsim Player file in \02_Model\ folder. 
	 GoldSim will import the data from the (.xlsx) files into the GoldSim player file and then execute.
3.   `03_Post_Adapter.py` will convert the Goldsim output files (.txt) back into XML format.

All of the above is just an example of how a simple adapter can be achieved. Using R or Java would also be possible.
Enter the C:\ command prompt and then `>>> pip install pandas` may be required if Python doesn't have the requisite modules.

---
![alt text](assets\workflow.png)
