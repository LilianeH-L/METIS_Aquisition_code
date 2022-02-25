import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

#Initialize datafram values
from numpy import long

temps = []
electrode_1 = []
electrode_2 = []
encod_1 = []


with open("Acquisition-1.txt") as f:
    compteur = 0 #Get count to increment time values

    lines = f.readlines() #Read lines from .txt file

    #Iterate through lines of .txt file
    #Replace \n and seperators
    #.txt file is contructed as such :
        # time | electrod_1 | electrod_2 | ... | electrod_n | encod_1 | encod_2 | ... | encod_n
    for element in lines:
        element = element.replace('\n', '')
        x = element.split(" | ")
        temps.append(int(x[0]))
        electrode_1.append(int(x[1]))
        encod_1.append(long(x[3]))

    #Iterate through time column to get time variation
    #Delete last value in new list - last value is the only one not modified by loop
    for i in range(len(temps)-1):
        variation = temps[i+1]-temps[i]
        compteur += variation
        temps[i] = compteur/1000

    del temps[-1]
    del electrode_1[-1]
    del encod_1[-1]

data = {'temps': temps, 'electrode_1': electrode_1, 'encod_1': encod_1}
df = pd.DataFrame(data)

df.plot.line(x='temps')
#plt.ylim(0, 4096)
plt.xlabel('Temps (s)')
plt.ylabel('Données')
plt.show()

data1= np.asarray([electrode_1])
np.save('data.npy', data1)

data2=np.load('data.npy')
plt.plot(data2[0])
plt.show()
