# -*- coding: utf-8 -*-
"""
Example of C Libraries for CCS Spectrometers in Python with CTypes

"""
import os
import time
import matplotlib.pyplot as plt
import numpy as np
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
integration_time=c_double(2)
lib.tlccs_setIntegrationTime(ccs_handle, integration_time)

def main():
    #start scan
    lib.tlccs_startScan(ccs_handle)

    wavelengths=(c_double*3648)()

    lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))

    #retrieve data
    data_array=(c_double*3648)()

    lib.tlccs_getScanData(ccs_handle, byref(data_array))

    #plot data
    plt.plot(wavelengths, data_array)

    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Intensity [a.u.]")
    plt.grid(True)
    plt.show()
    wavelengths_python = list(wavelengths)  #Change c type data to python data type
    data_array_python  = list(data_array)   #Change c type data to python data type
    temp_matrix = np.array([wavelengths_python, data_array_python])

    temp_matrix = np.transpose(temp_matrix)
    print(wavelengths_python)
    print(data_array_python)
    print(temp_matrix)
    np.savetxt('./Data/save1.txt', temp_matrix, delimiter='\t')
    plt.plot(wavelengths, data_array)

main()
#close
lib.tlccs_close (ccs_handle)

