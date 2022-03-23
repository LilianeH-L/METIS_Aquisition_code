import serial
import queue
import multiprocessing as mp
import numpy as np
import os
import timeit
import multiprocessing
import matplotlib.pyplot as plt

# Define variables
nbElectrodes = 2
nbEncoders = 4
for i in range(0,nbElectrodes):
    electrode=[]
    A=[]
    A.append(electrode)
for i in range(0,nbEncoders):
    encodeur=[]
    A.append(encodeur)



#def retrieveData():




# Check if serial port is open
# Put baud rate at 500k bits/s - 2 encoders and 1 electrode make up to 10 bytes per package
portOpen = False
while not portOpen:
    try:
        # Make sure COM port is correct (see in Gestionnaire de périphériques)
        arduino = serial.Serial(port='COM3', baudrate=1000000, timeout=None, xonxoff=False, rtscts=False,
                                dsrdtr=False)
        # Clear the serial buffer (input and output)
        arduino.flushInput()
        arduino.flushOutput()
        portOpen = True
    except:
        pass

# Create queue to hold in all the values sent over by the TeensyLC
que1 = queue.Queue()
print('Queue created, starting acquisition')

# Get the data and insert it in que1
try:
    start = timeit.default_timer()
    while True:
        #Get the number of bytes in the input buffer of the serial port
        bytesToRead = arduino.in_waiting
        if bytesToRead != 0:
            # Read the number of bytes in the input buffer
            data = arduino.read(bytesToRead)
            for i in range(len(data)):
                que1.put(data[i])


except KeyboardInterrupt:
    stop = timeit.default_timer()
    print(stop - start)
    print(que1.qsize() / (nbElectrodes*2 + nbEncoders*4)) # Nb of packs of data sent

    #Retrieve data
    listData = list(que1.queue)
    values = []
    counter = 0
    for i in range(0, int(len(listData) / (nbElectrodes*2 + nbEncoders*4))):
        for j in range(nbElectrodes):
            values.append(listData[counter] + (listData[counter + 1] << 8))
            counter += 2

        for k in range(nbEncoders):
            values.append((listData[counter]) + (listData[counter + 1] << 8) + (listData[counter + 2] << 16) + (
                            listData[counter + 3] << 24))
            counter += 4

    # Plot all values obtained
    for i in range(0, len(values) - (len(A)-1), len(A)):
        for j in range(0,len(values-len(A-1))):
            A[i].append(values[j])


    fig, axs = plt.subplots(nbElectrodes, nbEncoders)
    fig.suptitle('Resultats obtenus')
    numeroElectrode = 0
    numeroEncodeur=0
    for i in range(0, nbElectrodes-1):
        axs[0, numeroElectrode].plot(A[i])
        axs[0, numeroElectrode].set_title(f'Electrode {numeroElectrode}')
        numeroElectrode+=1
    for i in range(nbElectrodes,len(A)-1):
        axs[1, numeroEncodeur].plot(A[i])
        axs[1, numeroEncodeur].set_title(f'Encodeur {numeroEncodeur}')
    """"    
        axs[0, 1].plot(electrode2)
    axs[0, 1].set_title('Electrode 2')
    #axs[0, 2].plot(electrode3)
    #axs[0, 2].set_title('Electrode 3')
    #axs[0, 3].plot(electrode4)
    #axs[0, 3].set_title('Electrode 4')
    axs[1, 0].plot(encodeur1)
    axs[1, 0].set_title('Encodeur 1')
    axs[1, 1].plot(encodeur2)
    axs[1, 1].set_title('Encodeur 2')
    axs[1, 2].plot(encodeur3)
    axs[1, 2].set_title('Encodeur 3')
    axs[1, 3].plot(encodeur4)
    axs[1, 3].set_title('Encodeur 4')"""
    plt.show()
    print('Acquisition done')