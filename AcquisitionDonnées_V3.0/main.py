import serial
import queue
import timeit
import matplotlib.pyplot as plt

######################## Only lines to modify are right here ###############################
# Define variables
# Please note that encoders need to be 4 as of this version - 31 mars 2022
nbElectrodes = 2
nbEncoders = 4
############################################################################################


A=[]

for i in range(0,nbElectrodes):
    electrode=[]
    A.append(electrode)
for i in range(0,nbEncoders):
    encodeur=[]
    A.append(encodeur)
print(A)


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
    for i in range(0, len(values) - (len(A)-1), len(A)):
        for j in range(0, len(A)):
            A[j].append(values[i + j])

    print(A)

    fig, axs = plt.subplots(nbElectrodes)
    fig.suptitle('Resultats obtenus Electrodes')
    numeroElectrode = 0
    for i in range(0, nbElectrodes):
        axs[numeroElectrode].plot(A[i])
        axs[numeroElectrode].set_title(f'Electrode {numeroElectrode}')
        numeroElectrode+=1
    plt.show()

    fig, axs = plt.subplots(nbEncoders)
    fig.suptitle('Resultats obtenus Encodeurs')
    numeroEncodeur = 0
    for i in range(nbElectrodes, len(A)):
        axs[numeroEncodeur].plot(A[i])
        axs[numeroEncodeur].set_title(f'Encodeur {numeroEncodeur}')
        numeroEncodeur += 1
    plt.show()

    print('Acquisition done')
