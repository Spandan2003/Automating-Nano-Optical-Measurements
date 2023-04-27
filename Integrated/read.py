import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

def read1():
    file_path = 'css saved data 5_5.txt'
    sizeArr = np.loadtxt(file_path, max_rows=1, comments='!', dtype= str)
    print(sizeArr)
    xLen = int(sizeArr[1])
    yLen = int(sizeArr[2])
    df = pd.DataFrame(np.loadtxt(file_path))
    df.columns = ['Wavelengths']+[str(i%xLen)+","+str(i//int(xLen)) for i in range(xLen*yLen)]
    print(df)

    return df, xLen, yLen

def inten(matrix, xLen, yLen):          #Matrix contains the data, while xLen and yLen gives size of the 2d region
    maxIntensity = np.zeros((xLen, yLen))
    maxWave = np.zeros((xLen, yLen))
    for yCor in range(yLen):
        for xCor in range(xLen):
            maxwavelength = 0
            maxintensity = 0
            for i in range(len(matrix)):
                if(matrix[str(xCor)+','+str(yCor)][i]>maxintensity):
                    maxwavelength = matrix['Wavelengths'][i]
                    maxintensity = matrix[str(xCor)+','+str(yCor)][i]
            maxIntensity[yCor][xCor] = maxintensity
            maxWave[yCor][xCor]= maxwavelength
    print(maxIntensity, maxWave, sep='\n')
    return maxIntensity

def plot2d(matrix, xLen, yLen):         #Matrix contains the data, while xLen and yLen gives size of the 2d region
    figure, axis = plt.subplots(xLen, yLen) #Divide the plots into subplots
    for xCor in range(xLen):
        for yCor in range(yLen):
            axis[xCor, yCor].plot(matrix['Wavelengths'], matrix[str(xCor)+','+str(yCor)])
            axis[xCor, yCor].set_title(str(xCor)+','+str(yCor))
            axis[xCor, yCor ].tick_params(left = False, right = False , labelleft = False ,
                    labelbottom = False, bottom = False)
    plt.show()

def colorplot(matrix, xLen, yLen):
    def on_click(event):
        if event.button is MouseButton.LEFT:
            xmouse, ymouse = event.xdata, event.ydata
            xmouse, ymouse = round(xmouse), round(ymouse)
            print(xmouse, ymouse)
            plt.figure(1)
            plt.cla()
            plt.plot(matrix['Wavelengths'], matrix[str(xmouse)+","+str(ymouse)])
            plt.xlabel("Wavelength [nm]")
            plt.ylabel("Intensity [a.u.]")
            plt.title(str(xmouse)+','+str(ymouse))
            plt.grid(True)
            plt.show()

    
    figure0 = plt.figure(0)
    figure0.canvas.callbacks.connect('button_press_event', on_click)

    x = [i for i in range(xLen)]
    y = [j for j in range(yLen)]
    z = inten(matrix, xLen, yLen)

    X, Y = np.meshgrid(x, y)
    #plt.pcolor(X, Y, z)
    plt.imshow(z,origin='lower',interpolation='bilinear')
    plt.colorbar()
    plt.show()


matrix, xLen, yLen = read1()
plot2d(matrix, xLen, yLen)
colorplot(matrix, xLen, yLen)

