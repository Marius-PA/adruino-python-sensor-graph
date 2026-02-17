from serial import Serial
import numpy, turtle

with Serial('COM5', 115200, timeout=1) as ser:
    data = []
    b = 0
    for i in range(0, 360):
        line = ser.readline().decode('utf-8').strip()
        if line != '':
            if line == '0.00':
                data.append([b, 'N/A'])  # Append infinity for "Too far"
                b += 1
            else:
                data.append([b, float(line)])
                b += 1
        print(data)