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

electrode1 = []
electrode2 = []
electrode3 = []
electrode4 = []
encodeur1 = []
encodeur2 = []
encodeur3 = []
encodeur4 = []

#def retrieveData():




# Check if serial port is open
# Put baud rate at 500k bits/s - 2 encoders and 1 electrode make up to 10 bytes per package
portOpen = False
while not portOpen:
    try:
        # Make sure COM port is correct (see in Gestionnaire de périphériques)
        arduino = serial.Serial(port='COM7', baudrate=1000000, timeout=None, xonxoff=False, rtscts=False,
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
    for i in range(0, len(values) - 5, 6):
        electrode1.append(values[i])
        electrode2.append(values[i + 1])
        #electrode3.append(values[i + 2])
        #electrode4.append(values[i + 3])
        encodeur1.append(values[i + 2])
        encodeur2.append(values[i + 3])
        encodeur3.append(values[i + 4])
        encodeur4.append(values[i + 5])

    fig, axs = plt.subplots(2, 4)
    fig.suptitle('Resultats obtenus')
    axs[0, 0].plot(electrode1)
    axs[0, 0].set_title('Electrode 1')
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
    axs[1, 3].set_title('Encodeur 4')
    plt.show()
    print('Acquisition done')