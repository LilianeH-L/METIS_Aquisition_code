import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

temps=[]
donnee=[]




with open("Acquisition-2.txt") as f:
    compteur=0
    lines=f.readlines()
    for element in lines:
        element=element.replace('\n','')
        x=element.split(" | ")
        temps.append(int(x[0]))
        donnee.append(int(x[1]))

    for i in range(len(temps)-1):
        variation= temps[i+1]-temps[i]
        compteur+=variation
        temps[i]=compteur
    del temps[-1]
    del donnee[-1]

data={'temps': temps , 'donnée': donnee}
df= pd.DataFrame(data)
print(df)

ax = plt.gca()
ax.set_ylim([0, 4094])
df.plot(kind='line', x= 'temps', y='donnée', ax=ax)
plt.ylabel('Données')
plt.show()

data1= np.asarray([donnee])
np.save('data.npy', data1)

data2=np.load('data.npy')
plt.plot(data2[0])
plt.show()





