import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

numero_muscle=[]
donnee=[]



with open("Biceps-31-janvier.txt") as f:
    lines=f.readlines()
    for element in lines:
        element=element.replace('\n','')
        x=element.split(" ")
        numero_muscle.append(int(x[0]))
        donnee.append(int(x[1]))

data={'#muscle': numero_muscle , 'donnée': donnee}
df= pd.DataFrame(data)
index_list= list(df.index.values)
df['index']=index_list

print(df)

ax = plt.gca()
ax.set_ylim([0, 4094])
df.plot(kind='line', x= 'index', y='donnée', ax=ax)
plt.ylabel('Données')
plt.show()







