try:
    from Thorlabs_Nanomax.MDT_COMMAND_LIB import *
    import numpy as np
    import pandas as pd
    import time
    import matplotlib.pyplot as plt
    import os
    from numpy import savetxt
    from ctypes import *
    import timeit 

except OSError as ex:
    print("Warning:",ex)
    exit()

class Nanomax:
    def __init__(self, serialNumber=-1):
        devs = mdtListDevices()
        print(devs)
        if(len(devs)!=0 and len(devs[0])!=0):
            serialNumber = devs[0][0]
        self.hdl = mdtOpen(serialNumber,115200,3)
        if(self.hdl < 0):
            print("Connect Nanomax ",serialNumber, "fail" )
        else:
            print("Connect Nanomax ",serialNumber, "successful")
        
        self.isMdtOpen = mdtIsOpen(serialNumber)
        mdtSetXAxisMaxVoltage(self.hdl, 11)
        mdtSetYAxisMaxVoltage(self.hdl, 11)
        mdtSetZAxisMaxVoltage(self.hdl, 0.1)
        print("mdtIsOpen ",self.isMdtOpen)

        id = []
        self.idResult = mdtGetId(self.hdl, id)
        if(self.idResult<0):
            print("mdtGetId fail ",self.idResult)
        else:
            print("Nanomax ID = ",id[0])
        
        self.limVoltage = [0]
        self.limitVoltageResult = mdtGetLimtVoltage(self.hdl, self.limVoltage)
        if(self.limitVoltageResult<0):
            print("mdtGetLimtVoltage fail ",self.limitVoltageResult)
        else:
            print("mdtGetLimtVoltage ",self.limVoltage)
    

    def setX(self, x):
        result = mdtSetXAxisVoltage(self.hdl, x)
        if(result<0):
            print("mdtSetXAxisVoltage fail ", result)
        else:
            pass #print("mdtSetXAxisVoltage ", x)

    def setY(self, y):
        result = mdtSetYAxisVoltage(self.hdl, y)
        if(result<0):
            print("mdtSetYAxisVoltage fail ", result)
        else:
            pass #print("mdtSetYAxisVoltage ", y)

    def setZ(self, z):
        result = mdtSetZAxisVoltage(self.hdl, z)
        if(result<0):
            print("mdtSetZAxisVoltage fail ", result)
        else:
            pass #print("mdtSetZAxisVoltage ", z)

    def initializeVoltage(self, x, y, z):
        self.setX(x)
        self.setY(y)
        self.setZ(z)

class CCS:
    def __init__(self, integrationTime=10.0e-3):
        os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")
        self.lib = cdll.LoadLibrary("TLCCS_64.dll")

        self.ccs_handle=c_int(0)

        #documentation: C:\Program Files\IVI Foundation\VISA\Win64\TLCCS\Manual

        #Start Scan- Resource name will need to be adjusted
        #windows device manager -> NI-VISA USB Device -> Spectrometer -> Properties -> Details -> Device Instance ID
        self.lib.tlccs_init(b"USB0::0x1313::0x8087::M00796613::RAW", 1, 1, byref(self.ccs_handle))   

        #set integration time in  seconds, ranging from 1e-5 to 6e1
        integrationTime=c_double(integrationTime)
        self.lib.tlccs_setIntegrationTime(self.ccs_handle, integrationTime)

    def getWavelength(self):
        #start scan
        self.lib.tlccs_startScan(self.ccs_handle)

        wavelengths=(c_double*3648)()

        self.lib.tlccs_getWavelengthData(self.ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))
        wavelengths_python = list(wavelengths)  
        return wavelengths_python

    def read(self):
        #start scan
        self.lib.tlccs_startScan(self.ccs_handle)

        #retrieve data
        data_array=(c_double*3648)()
        self.lib.tlccs_getScanData(self.ccs_handle, byref(data_array))

        
        data_array_python  = list(data_array)
        return data_array_python



xLen = int(input("Cols:"))
yLen = int(input("Rows:"))
interval = 2
nanomax_obj = Nanomax(serialNumber="1908086985-03") #Detects automatically if MDT device present. If error occurs, manually fill in the value
ccs_obj = CCS(2)  #Give custom integration time else default 10.0e-3
nanomax_obj.initializeVoltage(0,0,0)
direction = 1   #means will move towards +X
xCor = 0
matrix = []
input("Click enter:")
wavelength = ccs_obj.getWavelength()
for yCor in range(yLen):
    nanomax_obj.setY(yCor*interval)
    rowResult = []
    if(xCor==-1):
        xCor=0
    elif(xCor==xLen):
        xCor=xLen-1
    while(0<=xCor<xLen):
        nanomax_obj.setX(xCor*interval)
        print([xCor*interval,yCor*interval])
        input()
        rowResult.append([xCor*interval,yCor*interval, ccs_obj.read()])
        xCor+=direction

    direction = -direction
    if(direction>0):
        matrix.append(list(reversed(rowResult)))
    else:
        matrix.append(rowResult)
nanomax_obj.initializeVoltage(0,0,0)


test = []     
result = []      
def store1():       #store in format 1
    for yCor in range(yLen):
        row = [yCor*interval]
        for xCor in range(xLen):
            for i in range(len(wavelength)):
                test.append([xCor, yCor, wavelength[i], matrix[yCor][xCor][2][i]])
    print(test)
    result = pd.DataFrame(test, columns=['xCor','yCor','Wavelengths', 'Intensity'])
    return result

def store2():   #store in FORMAT 2
    result = pd.DataFrame({'Wavelengths':(wavelength)}) 
    for yCor in range(yLen):
        for xCor in range(xLen):
            result[str(xCor)+","+str(yCor)]=matrix[yCor][xCor][2]
    print(result)
    return result
result = store2()
np.savetxt('...\Integrated\css test.txt',result, delimiter='\t', newline='\n', header=str(xLen)+"\t "+str(yLen))