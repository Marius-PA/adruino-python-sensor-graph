from pyparsing import line
from serial import Serial
import numpy, turtle

with Serial('COM5', 115200, timeout=1) as ser:
    values = []
    b = 0
    for i in range(0, 360):
        data = ser.readline().decode('utf-8').strip()
        
        if "," in data and data != '':
            angle_str, dist_str = data.split(",")
            angle = float(angle_str)
            dist = float(dist_str)
            values.append([angle, dist])
            print(values)
        
        #if data != '':
        #    print(float(dist))
        #    if line == '0.00':
        #        data.append([b, 'N/A'])  # Append infinity for "Too far"
        #        b += 1
        #    else:
        #        data.append([b, float(line)])
        #        b += 1
        #print(data)