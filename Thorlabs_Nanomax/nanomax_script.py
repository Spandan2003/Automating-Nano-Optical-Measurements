try:
    from MDT_COMMAND_LIB import *
    import time
except OSError as ex:
    print("Warning:",ex)
    exit()
def CommonFunc(serialNumber):       #Connect to stage and set default values (2,2,0.1)
   hdl = mdtOpen(serialNumber,115200,3)
   print(hdl)
   if(hdl < 0):
       print("Connect ",serialNumber, "fail" )
       return -1;
   else:
       print("Connect ",serialNumber, "successful")
   
   result = mdtIsOpen(serialNumber)
   mdtSetXAxisMaxVoltage(hdl, 2)
   mdtSetYAxisMaxVoltage(hdl, 2)
   mdtSetZAxisMaxVoltage(hdl, 0.1)
   print("mdtIsOpen ",result)

   id = []
   result = mdtGetId(hdl, id)
   if(result<0):
       print("mdtGetId fail ",result)
   else:
       print(id)
   
   limitVoltage = [0]
   result = mdtGetLimtVoltage(hdl, limitVoltage)
   if(result<0):
      print("mdtGetLimtVoltage fail ",result)
   else:
      print("mdtGetLimtVoltage ",limitVoltage)
   return hdl

def initializeVoltage(x,y,z, hdl): #function to set all 3 voltages and later functions for particluar axis
    setX(x, hdl)
    setY(y, hdl)
    setZ(z, hdl)

def setX(x, hdl):
    result = mdtSetXAxisVoltage(hdl, x)
    if(result<0):
       print("mdtSetXAxisVoltage fail ", result)
    else:
       print("mdtSetXAxisVoltage ", x)

def setY(y, hdl):
    result = mdtSetYAxisVoltage(hdl,y)
    if(result<0):
       print("mdtSetYAxisVoltage fail ", result)
    else:
       print("mdtSetYAxisVoltage ", y)

def setZ(z, hdl):
    result = mdtSetZAxisVoltage(hdl, z)
    if(result<0):
       print("mdtSetZAxisVoltage fail ", result)
    else:
       print("mdtSetZAxisVoltage ", z)

def read(hdl):              #Print the current position of the stage
    xyzVoltage = [[0],[0],[0]]
    mdtGetXAxisVoltage(hdl, xyzVoltage[0])
    mdtGetYAxisVoltage(hdl, xyzVoltage[1])
    mdtGetZAxisVoltage(hdl, xyzVoltage[2])
    return [xyzVoltage[1][0],xyzVoltage[0][0]]

print("Enter no. of rows and cols of matrix: ")     #Input the size of the matrix of readings we want to move
n = int(input("Cols:"))       
m = int(input("Rows:"))

devs = mdtListDevices()
#print(devs)
hdl = CommonFunc(serialNumber="1908086985-03") #Fill serial number of your model
initializeVoltage(0,0,0,hdl)

direct = 1                 #Determines if you are going left to right or opposite              
col = 0                    #Column number
matrix = []
t = read(hdl)
for row in range(m):        #row number
    setY(row/10, hdl)       #Move stage to correct row
    temp = []
    if(col==-1):            #If we cross end go back to edge
        col=0
    elif(col==n):
        col=n-1
    while(0<=col<n):
        setX(col/10, hdl)   #Move stage to correct column
        t = read(hdl)
        temp.append([row/10,col/10, t])
        col+=direct
        time.sleep(1)
    direct = -direct        #reverse direction
    if(direct>0):           #append row data to matrix
        matrix.append(list(reversed(temp)))
    else:
        matrix.append(temp)
[print(matrix[row]) for row in range(len(matrix))]
print(read(hdl))