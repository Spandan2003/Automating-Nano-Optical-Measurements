# -*- coding: utf-8 -*-
"""
Example of C Libraries for CCS Spectrometers in Python with CTypes

"""
from operator import index
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import savetxt
from ctypes import *
import timeit 

os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")
lib = cdll.LoadLibrary("TLCCS_64.dll")

ccs_handle=c_int(0)

#documentation: C:\Program Files\IVI Foundation\VISA\Win64\TLCCS\Manual

#Start Scan- Resource name will need to be adjusted
#windows device manager -> NI-VISA USB Device -> Spectrometer -> Properties -> Details -> Device Instance ID
lib.tlccs_init(b"USB0::0x1313::0x8087::M00796613::RAW", 1, 1, byref(ccs_handle))   

#set integration time in  seconds, ranging from 1e-5 to 6e1
integration_time=c_double(10.0e-3)
timeslices = 5
numberOfReading = 2
lib.tlccs_setIntegrationTime(ccs_handle, integration_time)

#start scan
def main():
    for count in range(numberOfReading):
        startTime = timeit.default_timer()
        #print(startTime)
        lib.tlccs_startScan(ccs_handle)

        wavelengths=(c_double*3648)()

        lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))

        #retrieve data
        data_array=(c_double*3648)()
        lib.tlccs_getScanData(ccs_handle, byref(data_array))

        #plot data
        wavelengths_python = np.ndarray((3648, ), 'f', wavelengths, order='C')  #Change float f to double
        data_array_python  = np.ndarray((3648, ), 'f', data_array, order='C')   #Change float f to double
        if(count==0):
            resMatrix = pd.DataFrame(data=wavelengths_python, columns=["Wavelengths"])
            resMatrix["t = "+str(count*timeslices)] = data_array_python
        else:
            resMatrix["t = "+str(count*timeslices)] = data_array_python
        print(resMatrix)
        stopTime = timeit.default_timer()
        np.savetxt('...Data\Timesliced data.txt', resMatrix, delimiter='\t')

main()
#close
lib.tlccs_close (ccs_handle)

