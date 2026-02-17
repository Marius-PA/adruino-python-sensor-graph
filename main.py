from serial import Serial
import numpy, turtle

with Serial('COM5', 115200, timeout=1) as ser:
    line = ser.readline()   # read a '\n' terminated line
    while True:
        line = ser.readline().decode('utf-8').strip()
        print(line)