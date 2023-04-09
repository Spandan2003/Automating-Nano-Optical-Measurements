from Thorlabs_Nanomax.MDT_COMMAND_LIB import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from numpy import savetxt
from ctypes import *
import timeit 

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

def scan(x, y):
    nanomax_obj = Nanomax(serialNumber="1908086985-03")
    nanomax_obj.initializeVoltage(0,0,0)
    nanomax_obj.setX(x)
    nanomax_obj.setY(y)
    

    #start scan
    lib.tlccs_startScan(ccs_handle)

    wavelengths=(c_double*3648)()

    lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))

    #retrieve data
    data_array=(c_double*3648)()

    lib.tlccs_getScanData(ccs_handle, byref(data_array))

    wavelengths_python = list(wavelengths)  #Change c type data to Python data
    data_array_python  = list(data_array)   #Change c type data to Python data
    temp_matrix = np.array([wavelengths_python, data_array_python])

    temp_matrix = np.transpose(temp_matrix)
    print(wavelengths_python)
    print(data_array_python)
    print(temp_matrix)
    return wavelengths, data_array

def grid(xLen, yLen):
    def on_click(event):
        if event.button is MouseButton.LEFT:
            xmouse, ymouse = event.xdata, event.ydata
            #xmouse, ymouse = round(xmouse), round(ymouse)
            plt.cla()
            plt.xlim([0,xLen])
            plt.ylim([0,yLen])
            plt.grid(True, 'both')
            plt.plot(xmouse, ymouse, '+b')
            print(xmouse, ymouse)
            wavelen, data = scan(xmouse, ymouse)
            plt.figure(1)
            plt.cla()
            plt.plot(wavelen, data)
            plt.xlabel("Wavelength [nm]")
            plt.ylabel("Intensity [a.u.]")
            plt.title(str(xmouse)+','+str(ymouse))
            plt.grid(True)
            plt.show()

    print(np.zeros((xLen, yLen), int))
    figure0 = plt.figure(0)
    figure0.canvas.callbacks.connect('button_press_event', on_click)


    X, Y = np.meshgrid(xLen, yLen)
    plt.plot()
    plt.xlim([0,xLen])
    plt.ylim([0,yLen])
    plt.grid(True, 'both')
    #plt.imshow(np.zeros((xLen, yLen)), origin='lower',interpolation='bilinear')
    plt.show()

maxVx = 10
maxVy = 10

grid(maxVx, maxVy)
os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")
lib = cdll.LoadLibrary("TLCCS_64.dll")

ccs_handle=c_int(0)

#documentation: C:\Program Files\IVI Foundation\VISA\Win64\TLCCS\Manual

#Start Scan- Resource name will need to be adjusted
#windows device manager -> NI-VISA USB Device -> Spectrometer -> Properties -> Details -> Device Instance ID
lib.tlccs_init(b"USB0::0x1313::0x8087::M00796613::RAW", 1, 1, byref(ccs_handle))   

#set integration time in  seconds, ranging from 1e-5 to 6e1
integration_time=c_double(2)
lib.tlccs_setIntegrationTime(ccs_handle, integration_time)

nanomax_obj = Nanomax(serialNumber="1908086985-03")
nanomax_obj.initializeVoltage(0,0,0)

#close
lib.tlccs_close (ccs_handle)